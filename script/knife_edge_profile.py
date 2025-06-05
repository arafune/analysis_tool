#!/usr/bin/env python3

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.special import erfc
from lmfit import Model
import xarray as xr
import xarray_lmfit
import argparse

"""Load the knife edge profile from the scpecified file."""


def load_profile(file_path: Path) -> xr.DataArray:
    """Load the knife edge profile from the specified file.


    Parameters
    ----------
    file_path
        file_path generated from knife_edge.py

    Returns
    -------
    xr.DataArray
        Measured data
    """
    header = ""
    data = []
    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#"):
                header = stripped
            elif stripped:
                row = [float(x) for x in stripped.split() if x.strip()]
                data.append(row)
    max_len = max(len(row) for row in data)
    array = np.full((len(data), max_len), np.nan)
    for i, row in enumerate(data):
        array[i, : len(row)] = row
    attrs = parse_metadata(header)
    z = np.linspace(
        attrs["start_z"],
        attrs["start_z"] + attrs["step_z"] * (array.shape[0] - 1),
        array.shape[0],
    )
    height = np.linspace(
        attrs["start_height"],
        attrs["start_height"] + attrs["step_height"] * (array.shape[1] - 1),
        array.shape[1],
    )
    return xr.DataArray(
        array, coords={"z": z, "height": height}, dims=["z", "height"], attrs=attrs
    )


def parse_metadata(header: list[str]) -> dict[str, float | str]:
    """Parse metadata from the header line.


    Parameters
    ----------
    header
        list of the header lines

    Returns
    -------
    dict[str, float | str]
        A dictionary containing parsed metadata, which is used to attrs of xr.DataArray
    """
    metadata = {}
    for item in header[1:].split(","):
        if ":" in item:
            key, value = item.split(":", 1)
            key = key.strip()
            value = value.strip()
            try:
                metadata[key] = float(value)
            except ValueError:
                metadata[key] = value
    return metadata


def erfc_model(x, amplitude, center, diameter):
    """
    Error function model for fitting.

    Args:
        x (np.ndarray): Input data.
        amplitude (float): Amplitude of the error function.
        center (float): Center of the error function.
        diameter (float): Diameter of the error function.

    Returns:
        np.ndarray: Evaluated error function values.
    """
    return (amplitude / 2) * erfc((x - center) * np.sqrt(2) / diameter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # initialize
    parser.add_argument(
        "--output", type=str, help="Output file name, (default value is fit_result.png"
    )
    parser.add_argument("file", type=Path)

    args = parser.parse_args()  # add argument
    if args.output:
        ouptut = args.output
    else:
        output = "fit_result.png"

    model = Model(erfc_model)

    data = load_profile(args.file)
    guess_amplitude = data.max().item()
    the_axis = [x for x in list(data.dims) if x != "z"][0]
    guess_center = data.coords[the_axis].mean()
    guess_diameter = 50

    params = model.make_params(
        amplitude=guess_amplitude, center=guess_center, diameter=guess_diameter
    )

    data_fit = data.fillna(0).xlm.modelfit(the_axis, model=model, params=params)

    fig_fit, ax_fit = plt.subplots(1, 2, figsize=(10, 5))
    data_fit["modelfit_best_fit"].plot(ax=ax_fit[0])
    data_fit.modelfit_coefficients.sel(param="diameter").plot(ax=ax_fit[1])
    fig_fit.tight_layout()
    fig_fit.suptitle(str(args.file))
    fig_fit.savefig(output, dpi=300)
