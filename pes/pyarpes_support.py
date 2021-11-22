#!/usr/bin/env python

"""pyarpes plugin for SpecsLab Prodigy"""

from pathlib import Path
from typing import no_type_check
from typing import Union, Optional, List, Tuple, Dict
import numpy as np
import xarray as xr
import re


def itx_common_head(itxdata: List[str]) -> Dict[str, str]:
    """Parse Common head part

    Parameters
    ----------
    itxdata : List[str]
        Contents of itx data file (return on readlines())

    Returns
    -------
    Dict[str, str]
        Common head data
    """
    common_params: Dict[str, str] = {}
    for line in itxdata:
        if line.startswith("X //Acquisition Parameters"):
            break
        else:
            linedata: List[str] = line[3:].split(":", maxsplit=1)
            common_params[linedata[0]] = linedata[1]
    return common_params


def itx_core(
    itxdata: List[str], common_attrs: Dict[str, str] = {}, multi: bool = False
) -> Union[xr.DataArray, List[xr.DataArray]]:
    section: str = ""
    params: Dict[str, str] = {}
    pixels: Tuple[int, int] = (0, 0)
    angle: np.ndarray
    energy: np.ndarray
    data: List[List[float]] = []
    datasets: List[xr.DataArray] = []
    name: str = ""
    for line in itxdata:
        if line.startswith("X //Acquisition Parameters"):
            section = "params"
            params = {}
        elif line.startswith("WAVES/S/N"):
            section = "data"
        if section == "params":
            linedata = line[3:].split("=", maxsplit=1)
            if len(linedata) > 2:
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
                if setscale[0] == "x":
                    angle = np.linspace(
                        float(setscale[1]), float(setscale[2]), num=pixels[0]
                    )
                    params["angle_unit"] = setscale[3]
                elif setscale[0] == "y":
                    energy = np.linspace(
                        float(setscale[1]), float(setscale[2]), num=pixels[1]
                    )
                    params["energy_unit"] = setscale[3]
                elif setscale[0] == "d":
                    attrs = common_attrs
                    attrs.update(params)
                    attrs["count_unit"] = setscale[3]
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
                elif line.startswith("BEGIN") or line.startswith("END"):
                    pass
                else:
                    data.append([float(i) for i in line.split()])
    if multi:
        return datasets
    return xr.DataArray(
        np.array(data), coords=coords, dims=["phi", "eV"], attrs=attrs, name=name
    )


def load_itx_single(path_to_file: str) -> xr.DataArray:
    with open(path_to_file, "rt") as itxfile:
        itxdata: List[str] = itxfile.readlines()
    common_head: Dict[str, str] = itx_common_head(itxdata)
    if itxdata.count("BEGIN") != 1:
        raise RuntimeError("This file contains multi spectra. Use load_itx_multi")
    return itx_core(itxdata, common_head, False)


def load_itx_multi(path_to_file: str) -> List[xr.DataArray]:
    with open(path_to_file, "rt") as itxfile:
        itxdata: List[str] = itxfile.readlines()
    common_head: Dict[str, str] = itx_common_head(itxdata)
    return itx_core(itxdata, common_head, True)


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
    params: Dict[str, str] = {}
    data: Union[List[float], np.ndarray] = []
    pixels: Optional[Tuple[int, int]] = None
    with open(path_to_file, "rt") as sp2file:
        for line in sp2file:
            if line.startswith("#"):
                try:
                    params[line[2:].split("=", maxsplit=1)[0]] = params[
                        line[2:].split("=", maxsplit=1)[1]
                    ]
                except IndexError:
                    pass
            elif line.startswith("P"):
                pass
            else:
                pixels = (int(line.split()[0]), int(line.split()[1]))
            if pixels:
                data.append(float(line))
    data = np.array(data).reshape(pixels)
    e_range = [float(i) for i in re.findall(r"-?[0-9]+\.?[0-9]*", params["X Range"])]
    a_range = [float(i) for i in re.findall(r"-?[0-9]+\.?[0-9]*", params["Y Range"])]
    if pixels:
        coords = {
            "phi": np.deg2rad(np.linspace(a_range[0], a_range[1], pixels[1])),
            "eV": np.linspace(e_range[0], e_range[1], pixels[0]),
        }
    return xr.DataArray(np.array(data), coords=coords, dims=["phi", "eV"], attrs=params)
