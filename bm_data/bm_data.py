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
            ├── TIMESTAMP
            ├── EXPOSURESTAMP
            └── BITENCODING
     /BG_SETUP/DATA_SOURCE_MANAGER/
        ├── PROCESSOR/AVERAGING_COUNT
        └── PROCESSOR/SUMMING_COUNT

"""

from datetime import datetime
from typing import TYPE_CHECKING

import h5py
import numpy as np
import xarray as xr

if TYPE_CHECKING:
    from numpy.typing import NDArray


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
        timestamp: datetime = parse_iso8601(
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
        return hdf5data_to_matrix(data / factor, numcols, numrows)

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
        matrix = hdf5data_to_matrix(
            data / 2 ** (bits_per_pixel - bits),
            numcols,
            numrows,
        )
    elif enc == "s32":
        matrix = hdf5data_to_matrix(data, numcols, numrows)
    else:
        msg = f"Unknown BITENCODING: {encoding}"
        raise ValueError(msg)
    matrix = hdf5data_to_matrix(data, numcols, numrows) * power_calibration_multiplier

    return xr.DataArray(
        matrix / summing_count,
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


def hdf5data_to_matrix(data: np.ndarray, width: int, height: int) -> np.ndarray:
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


def parse_iso8601(s: str) -> datetime:
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
