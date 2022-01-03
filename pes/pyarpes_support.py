#!/usr/bin/env python

"""pyarpes plugin for SpecsLab Prodigy"""
from __future__ import annotations

from pathlib import Path
from typing import no_type_check
import numpy as np
import xarray as xr
import re


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
    return common_params


def _itx_core(
    itxdata: list[str], common_attrs: dict[str, str] = {}, multi: bool = False
) -> xr.DataArray|list[xr.DataArray]:
    section: str = ""
    params: dict[str, str] = {}
    pixels: tuple[int, int] = (0, 0)
    angle: np.ndarray
    energy: np.ndarray
    data: list[list[float]] = []
    datasets: list[xr.DataArray] = []
    name: str = ""
    for line in itxdata:
        if line.startswith("X //Acquisition"):
            section = "params"
            params = {}
        elif line.startswith("WAVES/S/N"):
            section = "data"
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
                    attrs = common_attrs
                    attrs.update(params)
                    attrs["count_unit"] = (setscale[3])[2:-1]
                    coords = {"phi": np.deg2rad(angle), "eV": energy}
                    section = ""
                    if multi:
                        datasets.append(
                            xr.DataArray(
                                np.array(data),
                                coords=coords,
                                dims=["phi", "eV"],
                                attrs=attrs,
                                name=name,
                            )
                        )
                    else:
                        return xr.DataArray(
                            np.array(data),
                            coords=coords,
                            dims=["phi", "eV"],
                            attrs=attrs,
                            name=name,
                        )
            elif line.startswith("BEGIN"):
                pass
            elif line.startswith("END"):
                pass
            else:
                data.append([float(i) for i in line.split()])

    return datasets


def load_itx_single(path_to_file: str) -> xr.DataArray:
    with open(path_to_file, "rt") as itxfile:
        itxdata: list[str] = itxfile.readlines()
        itxdata = list(map(str.rstrip, itxdata))
    common_head: dict[str, str] = _itx_common_head(itxdata)
    if itxdata.count("BEGIN") != 1:
        raise RuntimeError("This file contains multi spectra. Use load_itx_multi")
    return _itx_core(itxdata, common_head, False)


def load_itx_multi(path_to_file: str) -> list[xr.DataArray]:
    with open(path_to_file, "rt") as itxfile:
        itxdata: list[str] = itxfile.readlines()
    common_head: dict[str, str] = _itx_common_head(itxdata)
    return _itx_core(itxdata, common_head, True)


def load_sp2_datatype(path_to_file: str) -> xr.DataArray:
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
    params: dict[str, str] = {}
    data: list[float]|np.ndarray = []
    pixels: tuple[int, int]|None = None
    with open(path_to_file, "rt") as sp2file:
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
    if pixels:
        coords = {
            "phi": np.deg2rad(np.linspace(a_range[0], a_range[1], pixels[0])),
            "eV": np.linspace(e_range[0], e_range[1], pixels[1]),
        }
    return xr.DataArray(np.array(data), coords=coords, dims=["phi", "eV"], attrs=params)
