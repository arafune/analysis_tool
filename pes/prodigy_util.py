#!/usr/bin/env python

"""pyarpes plugin for SpecsLab Prodigy"""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import xarray as xr

if TYPE_CHECKING:
    from _typeshed import StrOrLiteralStr

from numpy.typing import NDArray

__all__ = ["load_itx", "load_sp2"]


def _itx_common_head(itx_data: list[str]) -> dict[str, str | int | float]:
    """Parse Common head part

    Parameters
    ----------
    itx_data : list[str]
        Contents of itx data file (return on readlines())

    Returns
    -------
    dict[str, str | int | float]
        Common head data
    """
    common_params: dict[str, str | int | float] = {}
    for line in itx_data[1:]:
        if line.startswith("X //Acquisition Parameters"):
            break
        else:
            line_data: list[str] = line[4:].split(":", maxsplit=1)
            common_params[line_data[0]] = line_data[1].strip()
            # Comment の処理
    return common_params


def _itx_core(
    itx_data: list[str], common_attrs: dict[str, str | int | float] = {}
) -> xr.DataArray:
    """Parse itx file

    Parameters
    ----------
    itx_data : list[str]
        _description_
    common_attrs : dict[str, str], optional
        _description_, by default {}

    Returns
    -------
    xr.DataArray
        _description_
    """
    section: str = ""
    params: dict[str, str | int | float] = {}
    pixels: tuple[int, int] = (0, 0)
    angle: NDArray[np.float64]
    energy: NDArray[np.float64]
    data: list[list[float]] = []
    name: str = ""
    for line in itx_data:
        if line.startswith("X //"):
            section = "params"
        elif line.startswith("WAVES/S/N"):
            pixels = (
                int(line[11:].split(")")[0].split(",")[0]),
                int(line[11:].split(")")[0].split(",")[1]),
            )
            name = (line.split(maxsplit=1)[-1])[1:-1]
            section = "data"
            continue
        elif line.startswith("IGOR"):
            pass
        if section == "params":
            line_data = [i.strip() for i in line[4:].split("=", maxsplit=1)]
            if len(line_data) > 1:
                try:
                    params[line_data[0]] = int(line_data[1])
                except ValueError:
                    try:
                        params[line_data[0]] = float(line_data[1])
                    except ValueError:
                        params[line_data[0]] = line_data[1]
        elif section == "data":
            if line.startswith("X SetScale"):
                setscale = line.split(",", maxsplit=5)
                if "x" in setscale[0]:
                    angle = np.linspace(
                        float(setscale[1]), float(setscale[2]), num=pixels[0]
                    )
                    params["angle_unit"] = setscale[3].strip()[1:-1]
                elif "y" in setscale[0]:
                    if "I" in setscale[0]:
                        energy = np.linspace(
                            float(setscale[1]), float(setscale[2]), num=pixels[1]
                        )
                    elif "P" in setscale[0]:
                        energy = np.linspace(
                            float(setscale[1]),
                            float(setscale[1]) + float(setscale[2]) * (pixels[1] - 1),
                            num=pixels[1],
                        )
                    params["energy_unit"] = setscale[3].strip()[1:3]
                elif "d" in setscale[0]:
                    params["count_unit"] = setscale[3].strip()[1:-1]

            elif line.startswith("BEGIN"):
                pass
            elif line.startswith("END"):
                pass
            else:
                data.append([float(i) for i in line.split()])
    common_attrs["spectrum_type"] = "cut"
    attrs = common_attrs
    attrs.update(params)
    coords = {"phi": np.deg2rad(angle), "eV": energy}
    attrs["angle_unit"] = "rad (theta_y)"
    section = ""
    return xr.DataArray(
        np.array(data),
        coords=coords,
        dims=["phi", "eV"],
        attrs=attrs,
        name=name,
    )


def load_itx(
    path_to_file: Path | str, **kwargs: dict[str, str | int | float]
) -> xr.DataArray:
    """Load and parse the (single) itx data.

    Parameters
    ----------
    path_to_file : Path | str
        Path to itx file.

    Returns
    -------
    xr.DataArray
        _description_

    Raises
    ------
    RuntimeError
        _description_
    """
    with open(path_to_file, "rt") as itx_file:
        itx_data: list[str] = itx_file.readlines()
        itx_data = list(map(str.rstrip, itx_data))
    common_head: dict[str, str | int | float] = _itx_common_head(itx_data)
    if itx_data.count("BEGIN") != 1:
        raise RuntimeError(
            "This file contains multi spectra. Use the file Prodigy produces"
        )
    data = _itx_core(itx_data, common_head)
    for k, v in kwargs.items():
        data.attrs[k] = v
    return data


def load_sp2(
    path_to_file: Path | str, **kwargs: dict[str, str | int | float]
) -> xr.DataArray:
    """Load and parse sp2 file

    Parameters
    ----------
    path_to_file : Path | str
        Path to sp2 file

    Returns
    -------
    xr.DataArray
        _description_
    """
    params: dict[str, str | float] = {}
    data: list[float] = []
    pixels: tuple[int, int] | None = None
    with open(path_to_file, "rt", encoding="Windows-1252") as sp2file:
        for line in sp2file:
            if line.startswith("#"):
                try:
                    params[line[2:].split("=", maxsplit=1)[0].strip()] = int(
                        line[2:].split("=", maxsplit=1)[1].strip()
                    )
                except ValueError:
                    try:
                        params[line[2:].split("=", maxsplit=1)[0].strip()] = float(
                            line[2:].split("=", maxsplit=1)[1].strip()
                        )
                    except ValueError:
                        params[line[2:].split("=", maxsplit=1)[0].strip()] = (
                            line[2:].split("=", maxsplit=1)[1].strip()
                        )
                except IndexError:
                    pass
            elif line.startswith("P"):
                pass
            else:
                if pixels:
                    data.append(float(line))
                else:
                    pixels = (int(line.split()[1]), int(line.split()[0]))
    e_range = [float(i) for i in re.findall(r"-?[0-9]+\.?[0-9]*", params["X Range"])]
    a_range = [float(i) for i in re.findall(r"-?[0-9]+\.?[0-9]*", params["Y Range"])]
    params["spectrum_type"] = "cut"
    if pixels:
        coords = {
            "phi": np.deg2rad(np.linspace(a_range[0], a_range[1], pixels[0])),
            "eV": np.linspace(e_range[0], e_range[1], pixels[1]),
        }
    for k, v in kwargs.items():
        params[k] = v
    return xr.DataArray(
        np.array(data).reshape(pixels), coords=coords, dims=["phi", "eV"], attrs=params
    )


def parse_setscale(line: str) -> tuple[str, str, float, float, str]:
    """Parse setscale"""
    assert "SetScale" in line
    flag: str
    dim: str
    num1: float
    num2: float
    unit: str
    setscale = line.split(",", maxsplit=5)
    if "/I" in line:
        flag = "I"
    elif "/P" in line:
        flag = "P"
    else:
        flag = ""
    if "x" in setscale[0]:
        dim = "x"
    elif "y" in setscale[0]:
        dim = "y"
    elif "z" in setscale[0]:
        dim = "z"
    elif "t" in setscale[0]:
        dim = "t"
    elif "d" in setscale[0]:
        dim = "d"
    else:
        raise RuntimeError("Dimmension is not correct")
    unit = setscale[3].strip()[1:-1]
    num1 = float(setscale[1])
    num2 = float(setscale[2])
    return (flag, dim, num1, num2, unit)
