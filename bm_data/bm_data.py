"""Module for reading beam monitor (BM) data stored in HDF5 file.

This follows a specific structure used in some beamline experiments.

This module reproduces the functionality of the original MATLAB function
`readhdf5(frame, filename)` written for R2021b, including:
- Reading metadata (image size, pixel scales, encoding, etc.)
- Converting 1D raw data arrays into 2D images
- Applying bit depth scaling or power calibration factors
- Printing diagnostic information for each frame

Typical HDF5 structure expected:

    /BG_DATA/<frame>/
        ├── DATA
        └── RAWFRAME/
            ├── WIDTH
            ├── HEIGHT
            ├── PIXELSCALEXUM
            ├── PIXELSCALEYUM
            ├── ENERGY/
            │   └── POWER_CALIBRATION_MULTIPLIER
            └── BITENCODING


Example:
    >>> from bmData import readhdf5
    >>> I = readhdf5(frame=0, filename="example.h5")
    >>> print(I.shape)
    (1024, 1280)

Requirements:
    - Python 3.12+
    - h5py
    - numpy

"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import h5py
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from lmfit import Model

if TYPE_CHECKING:
    from lmfit.model import ModelResult
    from matplotlib.colors import Colormap
    from matplotlib.figure import Figure
    from numpy.typing import NDArray


def gauss2d(
    xy: tuple[float, float],
    amplitude: float,
    sigma_x: float,
    sigma_y: float,
    offset: float,
    x0: float,
    y0: float,
) -> NDArray[np.float64]:
    """2D Gaussian function for fitting."""
    x, y = xy
    return np.asarray(
        amplitude
        * np.exp(
            -(((x - x0) ** 2) / (2 * sigma_x**2) + ((y - y0) ** 2) / (2 * sigma_y**2)),
        )
        + offset,
        dtype=np.float64,
    )


gmodel = Model(gauss2d)


def bm_plot(
    data: xr.DataArray,
    pixel_radius: int = 30,
    figsize: tuple[float, float] = (15, 5),
    cmap: Colormap | str = "viridis",
) -> tuple[Figure, ModelResult]:
    """Plot beam monitor data with Gaussian fit overlay.

    Args:
        data (xr.DataArray): 2D beam monitor data.
        pixel_radius (int): Radius around the peak for fitting.
        figsize (tuple): Figure size.
        cmap (Coloramp | str): Colormap for the image.

    Returns:
        Figure, ModelResult: Matplotlib figure with the plot, and the fitting result.

    """
    fig: Figure = plt.figure(figsize=figsize)
    ax0 = fig.add_subplot(1, 3, 1)
    ax1 = fig.add_subplot(1, 3, 2)
    ax2 = fig.add_subplot(1, 3, 3)
    y_idx, x_idx = np.unravel_index(data.values.argmax(), data.shape)
    x0, y0 = float(data.x.values[x_idx]), float(data.y.values[y_idx])
    cropped = data.isel(
        {
            "x": slice(x_idx - pixel_radius, x_idx + pixel_radius),
            "y": slice(y_idx - pixel_radius, y_idx + pixel_radius),
        },
    )
    cropped.plot(
        ax=ax0,
        cmap=cmap,
        add_colorbar=False,
    )

    x, y = np.meshgrid(cropped.x.values, cropped.y.values)
    z = cropped.values

    params = gmodel.make_params(
        amplitude=z.max() - z.min(),
        sigma_x=5.0,
        sigma_y=5.0,
        offset=z.min(),
        x0=x0,
        y0=y0,
    )
    params["x0"].vary = True
    params["y0"].vary = True
    result = gmodel.fit(z.ravel(), params, xy=(x.ravel(), y.ravel()))
    fit_z = result.best_fit.reshape(z.shape)

    ax1.plot(cropped.x, z[pixel_radius, :], "o", label="Data")
    ax1.plot(cropped.x, fit_z[pixel_radius, :], "-", label="Fit")

    ax2.plot(cropped.y, z[:, pixel_radius], "o", label="Data")
    ax2.plot(cropped.y, fit_z[:, pixel_radius], "-", label="Fit")
    ax1.set_ylim((0.0, None))
    ax2.set_ylim((0.0, None))
    return fig, result


def modelresult_plot(
    modelresults: list[ModelResult],
    z_values: list[float],
    figsize: tuple[float, float] = (8, 4),
) -> Figure:
    """Plot the model fitting results.

    Args:
        modelresults (list[ModelResult]): List of model fitting results.
        z_values (list[float]): Corresponding z positions.
        figsize (tuple): Figure size.

    Returns:
        Figure: Matplotlib figure with the plots.

    """
    assert len(modelresults) == len(z_values)
    sigma_x = []
    sigma_y = []
    intensities = []
    for modelresult in modelresults:
        sigma_x.append(modelresult.params["sigma_x"].value)
        sigma_y.append(modelresult.params["sigma_y"].value)
        intensities.append(modelresult.params["amplitude"].value)

    fig = plt.figure(figsize=figsize)
    ax0 = fig.add_subplot(1, 3, 1)
    ax0.plot(z_values, np.array(sigma_x) * 2.35482, label=r"$FWHM_x$")
    ax0.plot(z_values, np.array(sigma_y) * 2.35482, label=r"$FWHM_y$")
    ax0.set_title("FWHM")
    ax0.legend()
    ax0.set_xlabel("z (mm)")
    ax0.set_ylabel(r"FWHM ($\mu$m)")

    ax1 = fig.add_subplot(1, 3, 2)
    ax1.scatter(
        z_values,
        1 / (np.array(sigma_x) * np.array(sigma_y)),
        color="red",
    )
    ax1.set_title("Beam Sharpness (a.u.)")
    ax1.set_xlabel("z (mm)")

    ax2 = fig.add_subplot(1, 3, 3)
    ax2.scatter(z_values, intensities, label="Intensity", color="green")
    ax2.set_title("Intensity")
    return fig


def readhdf5(filename: str, frame: int = 1) -> xr.DataArray:
    """Read a beam monitor (BM) frame from an HDF5 file.

    This function reproduces the behavior of the MATLAB `readhdf5`
    function that reads a specific hierarchical HDF5 structure.

    The function automatically:
        - Retrieves geometry and calibration metadata
        - Decodes the raw frame according to `BITENCODING`
        - Applies optional power calibration
        - Returns the image as a 2D NumPy array

    Args:
        frame (int): Frame index under `/BG_DATA/<frame>/`.
        filename (str): Path to the HDF5 file.

    Returns:
        np.ndarray: 2D image array (height x width) after decoding and calibration.

    Raises:
        FileNotFoundError: If the file cannot be opened.
        KeyError: If expected HDF5 paths are missing.
        ValueError: If an unknown bit encoding is encountered or data size mismatch.

    Notes:
        Supported `BITENCODING` values include:
            {'L8', 'L16_8', 'L16_10', 'L16_12', 'L16_14', 'L16_16', 'L16',
             'R8', 'R16_8', 'R16_10', 'R16_12', 'R16_14', 'R16_16', 'R16',
             'S16_14', 'S16_16', 'S32'}

        The function prints diagnostic values similar to the MATLAB version
        using the internal `screendump` function.

    Example:
        >>> I = readhdf5(0, "data/example.h5")
        >>> print(I.shape)
        (2048, 2048)

    """
    with h5py.File(filename, "r") as f:
        group = f[f"/BG_DATA/{frame}"]

        numcols: int = group["RAWFRAME/WIDTH"][()].item()
        numrows: int = group["RAWFRAME/HEIGHT"][()].item()
        assert isinstance(numcols, int)
        assert isinstance(numrows, int)
        pixelscalexum: float = group["RAWFRAME/PIXELSCALEXUM"][()].item()
        pixelscaleyum: float = group["RAWFRAME/PIXELSCALEYUM"][()].item()
        assert isinstance(pixelscalexum, float)
        assert isinstance(pixelscaleyum, float)
        y_axis: NDArray[np.float64] = np.linspace(
            0,
            numrows * (pixelscalexum - 1),
            numrows,
        )
        x_axis: NDArray[np.float64] = np.linspace(
            0,
            numcols * (pixelscaleyum - 1),
            numcols,
        )
        timestamp: datetime = _parse_iso8601(
            group["RAWFRAME/TIMESTAMP"][()].astype(str).item(),
        )
        exposurestamp: float = group["RAWFRAME/EXPOSURESTAMP"][()].item()

        data: np.ndarray = group["DATA"][()]  # 1D array
        power_calibration_multiplier: float = group[
            "RAWFRAME/ENERGY/POWER_CALIBRATION_MULTIPLIER"
        ][()].item()

        encoding: str = group["RAWFRAME/BITENCODING"][()].astype(str).item()
        setting = f["/BG_SETUP/DATA_SOURCE_MANAGER"]
        average_count: int = setting["PROCESSOR/AVERAGING_COUNT"][()].item()
        summing_count: int = setting["PROCESSOR/SUMMING_COUNT"][()].item()

    assert isinstance(encoding, str)
    bits_per_pixel = 32
    power_calibration_multiplier = 10 ** (power_calibration_multiplier / 10)
    assert isinstance(power_calibration_multiplier, float)

    def scale_and_reshape(bits: int) -> np.ndarray:
        """Return the matrix normalize by bit depth and reshape."""
        factor: float = 2 ** (bits_per_pixel - bits - 1)
        return _hdf5data_to_matrix(data / factor, numcols, numrows)

    enc = encoding.lower()
    bit_map = {
        "l8": 8,
        "r8": 8,
        "l16_8": 8,
        "r16_8": 8,
        "l16_10": 10,
        "r16_10": 10,
        "l16_12": 12,
        "r16_12": 12,
        "l16_14": 14,
        "r16_14": 14,
        "l16_16": 16,
        "r16_16": 16,
        "l16": 16,
        "r16": 16,
    }
    if enc in bit_map:
        matrix = scale_and_reshape(bit_map[enc])
    elif enc in {"s16_14", "s16_16"}:
        bits = 14 if enc == "s16_14" else 16
        matrix = _hdf5data_to_matrix(
            data / 2 ** (bits_per_pixel - bits),
            numcols,
            numrows,
        )
    elif enc == "s32":
        matrix = _hdf5data_to_matrix(data, numcols, numrows)
    else:
        msg = f"Unknown BITENCODING: {encoding}"
        raise ValueError(msg)
    matrix = _hdf5data_to_matrix(data, numcols, numrows) * power_calibration_multiplier

    return xr.DataArray(
        matrix / summing_count / exposurestamp,
        dims=("y", "x"),
        coords={"x": x_axis, "y": y_axis},
        name="normalized intensity",
        attrs={
            "average_count": average_count,
            "summing_count": summing_count,
            "timestamp": timestamp,
            "exposure_stamp": exposurestamp,
        },
    )


def _hdf5data_to_matrix(data: np.ndarray, width: int, height: int) -> np.ndarray:
    """Convert a 1D HDF5 data array into a 2D image.

    Args:
        data (np.ndarray): 1D array containing pixel values.
        width (int): Image width (number of columns).
        height (int): Image height (number of rows).

    Returns:
        np.ndarray: 2D NumPy array of shape (height, width).

    Raises:
        ValueError: If data length does not match width x height.

    """
    data = np.asarray(data)
    if data.size != width * height:
        msg = "Data size does not match WIDTH x HEIGHT."
        raise ValueError(msg)
    return data.reshape((height, width))


def _parse_iso8601(s: str) -> datetime:
    if "." in s:
        date_part, rest = s.split(".", 1)
        microsec_and_tz = rest.split("+") if "+" in rest else rest.split("-")
        microsec = microsec_and_tz[0][:6]  # 6桁に切り捨て
        tz = (
            "+" + microsec_and_tz[1]
            if "+" in rest
            else "-" + microsec_and_tz[1]
            if "-" in rest
            else ""
        )
        s_fixed = f"{date_part}.{microsec}{tz}"
    else:
        s_fixed = s
    return datetime.fromisoformat(s_fixed)
