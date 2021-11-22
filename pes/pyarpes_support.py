#!/usr/bin/env python


"""pyarpes plugin for SpecsLab Prodigy"""

from pathlib import Path
from typing import no_type_check
from typing import Union
import numpy as np
import xarray as xr


def load_itx_datatype(path_to_file: str) -> Union[xr.DataArray, list[xr.DataArray]]:
    """[summary]

    Parameters
    ----------
    path_to_file : str
        [description]

    Returns
    -------
    list[xr.DataArray]
        [description]
    """
    ## itxファイルは複数のスペクトルデータを含むので、一度全部読み込んで、内容を解析する必要がある？
    ## 形式は以下のようになっている。
    ##  IGOR
    ##  X //Created Date (UTC): 2021-Nov-18 12:53:08.227474
    ##  X //Igor Text File Exporter Version: 0.3
    ##  X //Created by: SpecsLab Prodigy, Version 4.84.2-r101696
    ##  X //Acquisition Parameters:
    ##  X //Scan Mode         = Fixed Analyzer Transmission
    ##  X //User Comment      = beta=-7(190)
    ##  X //Analysis Mode     = UPS
    ##  X //Lens Mode         = WideAngleMode
    ##  X //Lens Voltage      = 40V
    ##  X //Spectrum ID       = 17
    ##  X //Analyzer Slits    = 1:0.5x20\B:open
    ##  X //Number of Scans   = 20
    ##  X //Number of Samples = 701
    ##  X //Scan Step         = 0.002
    ##  X //DwellTime         = 0.096
    ##  X //Excitation Energy = 5.94
    ##  X //Kinetic Energy    = 4.8
    ##  X //Binding Energy    = 1.14
    ##  X //Pass Energy       = 2
    ##  X //Bias Voltage      = -1.5
    ##  X //Detector Voltage  = 1500
    ##  X //WorkFunction      = 4.401
    ##  WAVES/S/N=(600,701) 'Spectrum_15_1'
    ##  BEGIN
    ##  .....
    ##  END
    ##  X SetScale/I x, -12.4792, 12.4792, "deg (theta_y)", 'Spectrum_15_1'
    ##  X SetScale/I y, 4.8, 6.2, "eV (Kinetic Energy)", 'Spectrum_15_1'
    ##  X SetScale/I d, 0, 1375.24, "cps (Intensity)", 'Spectrum_15_1'
    ##  X //Acquisition Parameters:
    ##  X //Scan Mode         = Fixed Analyzer Transmission
    ##  X //User Comment      = beta=-7(190), remeasure
    ##  X //Analysis Mode     = UPS
    ##  X //Lens Mode         = WideAngleMode
    ##  X //Lens Voltage      = 40V
    ##  X //Spectrum ID       = 18
    ##  ...
    ##  2つめ以降は // Acquisition Parameters: から始まることに注意。
    with open(path_to_file, "rt") as itxfile:
        itxdata: list[str] = itxfile.readlines()
        # "BEGIN" の文字列の個数。
        n_spectra: int = itxdata.count("BEGIN")
        section: str = ""
        datasets: list[xr.DataArray] = []
        common_params: dict[str, str] = {}
        meas_params: dict[str, str] = {}
        pixels: tuple[int, int] = (0, 0)
        angle: np.ndarray
        energy: np.ndarray
        data: list[list[float]] = []
        for line in itxdata:
            if line.startswith("X //Created Date (UTC):"):
                section = "Common"
                common_params = {}
            elif line.startswith("X //Acquisition Parameters"):
                section = "meas_params"
                meas_params = {}
            elif line.startswith("WAVES/S/N"):
                section = "data"
                data = []
            if section is "Common":
                linedata: list[str] = line[3:].split(":", maxsplit=1)
                common_params[linedata[0]] = linedata[1]
            elif section is "meas_param":
                linedata = line[3:].split("=", maxsplit=1)
                try:
                    meas_params[linedata[0]] = linedata[1]
                except IndexError:
                    pass
            elif section is "data":
                if line.startswith("WAVES/S/N"):
                    pixels = tuple([int(i) for i in line[11:].split(")")[0].split(",")])
                elif line.startswith("X SetScale"):
                    # 単位、角度、エネルギー範囲を読み取る
                    setscale = line.split(",", maxsplit=5)
                    if setscale[0] == "x":
                        angle = np.linspace(
                            float(setscale[1]), float(setscale[2]), num=pixels[0]
                        )
                        meas_params["angle_unit"] = setscale[3]
                    elif setscale[0] == "y":
                        energy = np.linspace(
                            float(setscale[1]), float(setscale[2]), num=pixels[1]
                        )
                        meas_params["energy_unit"] = setscale[3]
                    elif setscale[0] == "d":
                        attrs: dict[str, str] = {}
                        attrs.update(common_params)
                        attrs.update(meas_params)
                        attrs["count_unit"] = setscale[3]  # count_unit
                        coords = {"phi": np.deg2rad(angle), "eV": energy}
                        datasets.append(
                            xr.DataArray(
                                np.array(data),
                                coords=coords,
                                dims=["phi", "eV"],
                                attrs=attrs,
                            )
                        )
                        section = ""
                    pass
                elif line.startswith("BEGIN"):
                    pass
                elif line.startswith("END"):
                    pass
                else:
                    data.append([float(i) for i in line.split()])
    if len(datasets) == 1:
        return datasets[0]
    else:
        return datasets


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
    pass
