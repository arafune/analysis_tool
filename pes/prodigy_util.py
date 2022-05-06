#!/usr/bin/env python

"""pyarpes plugin for SpecsLab Prodigy"""
from __future__ import annotations

from pathlib import Path
from typing import no_type_check
import numpy as np
import xarray as xr
import re

__all__ = ["load_itx", "load_sp2"]


def _itx_common_head(itxdata: list[str]) -> dict[str, str]:
    """Parse Common head part

    Parameters
    ----------
    itxdata : list[str]
        Contents of itx data file (return on readlines())

    Returns
    -------
    Dict[str, str]
        Common head data
    """
    common_params: dict[str, str] = {}
    for line in itxdata[1:]:
        if line.startswith("X //Acquisition Parameters"):
            break
        else:
            linedata: list[str] = line[4:].split(":", maxsplit=1)
            common_params[linedata[0]] = linedata[1].strip()
            # Comment の処理
    return common_params


def _itx_core(itxdata: list[str], common_attrs: dict[str, str] = {}) -> xr.DataArray:
    """_summary_

    Parameters
    ----------
    itxdata : list[str]
        _description_
    common_attrs : dict[str, str], optional
        _description_, by default {}

    Returns
    -------
    xr.DataArray
        _description_
    """
    section: str = ""
    params: dict[str, str] = {}
    pixels: tuple[int, int] = (0, 0)
    angle: np.ndarray
    energy: np.ndarray
    data: list[list[float]] = []
    name: str = ""
    params = {}
    for line in itxdata:
        if line.startswith("X //"):
            section = "params"
        elif line.startswith("WAVES/S/N"):
            section = "data"
        elif line.startswith("IGOR"):
            pass
        if section == "params":
            linedata = [i.strip() for i in line[4:].split("=", maxsplit=1)]
            if len(linedata) > 1:
                try:
                    params[linedata[0]] = int(linedata[1])
                except ValueError:
                    try:
                        params[linedata[0]] = float(linedata[1])
                    except ValueError:
                        params[linedata[0]] = linedata[1]
        elif section == "data":
            if line.startswith("WAVES/S/N"):
                pixels = (
                    int(line[11:].split(")")[0].split(",")[0]),
                    int(line[11:].split(")")[0].split(",")[1]),
                )
                name = (line.split(maxsplit=1)[-1])[1:-1]
            elif line.startswith("X SetScale"):
                setscale = line.split(",", maxsplit=5)
                if "x" in setscale[0]:
                    angle = np.linspace(
                        float(setscale[1]), float(setscale[2]), num=pixels[0]
                    )
                    params["angle_unit"] = setscale[3][2:-1]
                elif "y" in setscale[0]:
                    energy = np.linspace(
                        float(setscale[1]), float(setscale[2]), num=pixels[1]
                    )
                    params["energy_unit"] = setscale[3][2:-1]
                elif "d" in setscale[0]:
                    params["count_unit"] = setscale[3][2:-1]

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
    return xr.DataArray(  ##  ここでは単にDataArray を返す。複数Waveのバージョンはこの関数を繰り返すだけで良いわけだから。
        np.array(data),
        coords=coords,
        dims=["phi", "eV"],
        attrs=attrs,
        name=name,
    )


def load_itx(path_to_file: str, **kwargs: dict[str, str | float]) -> xr.DataArray:
    """_summary_

    Parameters
    ----------
    path_to_file : str
        _description_

    Returns
    -------
    xr.DataArray
        _description_

    Raises
    ------
    RuntimeError
        _description_
    """
    with open(path_to_file, "rt") as itxfile:
        itxdata: list[str] = itxfile.readlines()
        itxdata = list(map(str.rstrip, itxdata))
    common_head: dict[str, str] = _itx_common_head(itxdata)
    if itxdata.count("BEGIN") != 1:
        raise RuntimeError("This file contains multi spectra. Use load_itx_multi")
    data = _itx_core(itxdata, common_head)
    for k, v in kwargs.items():
        data.attrs[k] = v
    return data


def load_sp2(path_to_file: str, **kwags: dict[str, str | float]) -> xr.DataArray:
    """sp2 file loader

    sp2 file contains the "single" spectrum data

    Parameters
    ----------
    path_to_file : str
        [description]

    Returns
    -------
    xr.DataArray
        [description]
    """
    params: dict[str, str | float] = {}
    data: list[float] | np.ndarray = []
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
    data = np.array(data).reshape(pixels)
    e_range = [float(i) for i in re.findall(r"-?[0-9]+\.?[0-9]*", params["X Range"])]
    a_range = [float(i) for i in re.findall(r"-?[0-9]+\.?[0-9]*", params["Y Range"])]
    params["spectrum_type"] = "cut"
    if pixels:
        coords = {
            "phi": np.deg2rad(np.linspace(a_range[0], a_range[1], pixels[0])),
            "eV": np.linspace(e_range[0], e_range[1], pixels[1]),
        }
    for k, v in kwags:
        params[k] = v
    return xr.DataArray(np.array(data), coords=coords, dims=["phi", "eV"], attrs=params)
