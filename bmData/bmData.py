"""Module for reading beam monitor (BM) data stored in HDF5 files
that follow a specific structure used in some beamline experiments.

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

import h5py
import numpy as np


def readhdf5(frame: int, filename: str) -> np.ndarray:
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

        numcols = int(group["RAWFRAME/WIDTH"][()])
        numrows = int(group["RAWFRAME/HEIGHT"][()])
        pixelscalexum = float(group["RAWFRAME/PIXELSCALEXUM"][()])
        pixelscaleyum = float(group["RAWFRAME/PIXELSCALEYUM"][()])
        data = group["DATA"][()]  # 1D array
        power_calibration_multiplier = float(
            group["RAWFRAME/ENERGY/POWER_CALIBRATION_MULTIPLIER"][()]
        )
        encoding = group["RAWFRAME/BITENCODING"][()].astype(str).strip()

    BitsPerPixel = 32

    if power_calibration_multiplier == 0:
        power_calibration_multiplier = 1.0

        def scale_and_reshape(data, bits):
            """Internal helper to normalize by bit depth and reshape."""
            factor = 2 ** (BitsPerPixel - bits - 1)
            return hdf5data_to_matrix(data / factor, numcols, numrows)

        enc = encoding.lower()
        if enc in {"l8", "l16_8", "r8", "r16_8"}:
            I = scale_and_reshape(data, 8)
        elif enc in {"l16_10", "r16_10"}:
            I = scale_and_reshape(data, 10)
        elif enc in {"l16_12", "r16_12"}:
            I = scale_and_reshape(data, 12)
        elif enc in {"l16_14", "r16_14"}:
            I = scale_and_reshape(data, 14)
        elif enc in {"l16_16", "l16", "r16_16", "r16"}:
            I = scale_and_reshape(data, 16)
        elif enc == "s16_14":
            I = hdf5data_to_matrix(data / 2 ** (BitsPerPixel - 14), numcols, numrows)
        elif enc == "s16_16":
            I = hdf5data_to_matrix(data / 2 ** (BitsPerPixel - 16), numcols, numrows)
        elif enc == "s32":
            I = hdf5data_to_matrix(data, numcols, numrows)
        else:
            raise ValueError(f"Unknown BITENCODING: {encoding}")
    else:
        I = hdf5data_to_matrix(data, numcols, numrows)
        I *= power_calibration_multiplier

    # Print diagnostics
    screendump("numrows", numrows)
    screendump("numcols", numcols)
    screendump("I(1,1)", I[0, 0])
    screendump("encoding", encoding)
    screendump("pixelscalexum", pixelscalexum)
    screendump("pixelscaleyum", pixelscaleyum)
    screendump("power_calibration_multiplier", power_calibration_multiplier)

    return I


def hdf5data_to_matrix(data: np.ndarray, width: int, height: int) -> np.ndarray:
    """Convert a 1D HDF5 data array into a 2D image.

    Args:
        data (np.ndarray): 1D array containing pixel values.
        width (int): Image width (number of columns).
        height (int): Image height (number of rows).

    Returns:
        np.ndarray: 2D NumPy array of shape (height, width).

    Raises:
        ValueError: If data length does not match width × height.
    """
    data = np.asarray(data)
    if data.size != width * height:
        raise ValueError("Data size does not match WIDTH × HEIGHT.")
    return data.reshape((height, width))


def screendump(name: str, value):
    """Print variable name and value to console (MATLAB screendump equivalent).

    Args:
        name (str): Variable name to display.
        value (Any): Variable value to print. Strings and numerics are formatted differently.
    """
    if isinstance(value, str):
        print(f"{name} = {value}")
    else:
        print(f"{name} = {value:.4f}")
