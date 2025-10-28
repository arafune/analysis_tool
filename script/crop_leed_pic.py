#! /usr/bin/env python3
"""Convert to tiff image file from the LEED picture taken by EOS Kiss X5

The "correction" functionality, which the commercial cameras have, it
needless one.

(To reresent the intensity as the charge of the CCD, such "correction functionality"
should be removed.)

So, this code:
    * No white balance added
    * No auto scale added
    * No auto bright added
    * 16 bit (The brightest is 65536.)

to evaluate numerically.


How to use
On windows:

$items = Get-ChildItem . -File *.CR2

foreach ($item in $items) {
python3 crop_leed_pic.py $item
}

Mac & Linux:
(as usual)

"""

import argparse
import pathlib

import imageio
import numpy as np
import rawpy
from numpy.typing import NDArray

from scipy.ndimage import median_filter
from scipy.ndimage import uniform_filter

from scipy.ndimage import uniform_filter, binary_dilation


def remove_cluster_spikes(arr, inner_size=3, outer_size=5, diff_threshold=300):
    """Remove clustered (3x3) high-intensity spikes.

    By replacing them with the average of surrounding pixels outside the cluster.

    Parameters
    ----------
    arr : 2D np.ndarray
        Input array.
    inner_size : int
        Size of the spike cluster to detect (e.g., 3 for 3x3).
    outer_size : int
        Size of the region used to compute the surrounding average (e.g., 5 for 5x5).
    diff_threshold : float
        Intensity difference threshold for detecting spike clusters.

    Returns
    -------
    np.ndarray
        Array with clustered spikes replaced by surrounding mean values.
    """
    arr = np.asarray(arr)
    arr_filtered = arr.copy()

    # Local mean using the inner (3x3) window
    local_mean_inner = uniform_filter(arr, size=inner_size)

    # Local mean using the outer (5x5) window
    local_mean_outer = uniform_filter(arr, size=outer_size)

    # Detect regions where the inner region is much brighter than its surroundings
    mask = (local_mean_inner - local_mean_outer) > diff_threshold

    # Expand mask slightly to cover the whole spike cluster
    mask_dilated = binary_dilation(mask, structure=np.ones((inner_size, inner_size)))

    # Replace masked (spike) pixels with the outer local mean
    arr_filtered[mask_dilated] = local_mean_outer[mask_dilated]

    return arr_filtered


def remove_spikes(arr, size=3, threshold=3.0):
    mean = uniform_filter(arr, size=size)
    sq_mean = uniform_filter(arr**2, size=size)
    std = np.sqrt(sq_mean - mean**2)
    mask = np.abs(arr - mean) > threshold * std
    arr_filtered = arr.copy()
    arr_filtered[mask] = mean[mask]
    return arr_filtered


def remove_spikes_local_mean(arr, diff_threshold=500):
    local_mean = uniform_filter(arr, size=3)
    mask = (arr - local_mean) > diff_threshold
    arr_filtered = arr.copy()
    arr_filtered[mask] = 0
    return arr_filtered


def crop(
    pic: NDArray[np.float64],
    x: int = 912,
    y: int = 1866,
    side_length: int = 1600,
) -> NDArray[np.float64]:
    """Return cropping data of the gray scale.

    Note that the x- and y- coordinates are flipped judged by using standard
    image viewers.

    Parameters
    ----------
    pic: NDArray
        grayscale data
    x: int
        x-point of the corner
    y: int
        y-point of the corner
    side_length: int
        the length of the square side

    Returns
    -------
    NDArray

    """
    if pic.ndim == 2:
        return pic[x : x + side_length, y : y + side_length]
    elif pic.ndim == 3:
        return pic[x : x + side_length, y : y + side_length, :]
    msg = "The dimension of pic is invalid."
    raise RuntimeError(msg)


def chose_single_color(
    rgb: NDArray[np.float64], color: str = "G"
) -> NDArray[np.float64]:
    """Return single color data.

    Parameters
    ----------
    rgb: NDArray
    color: str
        'R', 'G', or 'B'

    Returns
    -------
    NDArray
    """
    color = color.upper()
    if color == "R":
        return rgb[:, :, 0]
    elif color == "G":
        return rgb[:, :, 1]
    elif color == "B":
        return rgb[:, :, 2]
    msg = f"Color {color} is invalid."
    raise RuntimeError(msg)


def rgb2sum(rgb: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the sum of RGB channels.

    Parameters
    ----------
    rgb: NDArray

    Returns
    -------
    NDArray

    """
    return rgb[:, :, 0] + rgb[:, :, 1] + rgb[:, :, 2]


def rgb2gray(rgb: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return Gray scale data.

    0.2989 * R + 0.5870 * G + 0.1140 * B
    is the Matlab algorithm.  While it seems reasonable, it is not
    taken here for keeping the linearity.

    Parameters
    ----------
    rgb: NDArray

    Returns
    -------
    NDArray

    """
    return rgb[:, :, 0] * 0.2989 + rgb[:, :, 1] * 0.5870 + rgb[:, :, 2] * 0.1140


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    _ = parse.add_argument("CR2file", help="CR2 file of the LEED picture", nargs="*")
    _ = parse.add_argument(
        "--color",
        help="""Color tiff output.
If not specified, gray scale tiff is output.  The other options are:
R or G or B: The Red (or Gree, Blue) channel only tiff output.
sum: The sum of RGB channels tiff output.""",
    )

    args = parse.parse_args()
    for cr2_file in args.CR2file:
        p = pathlib.Path(cr2_file)
        raw_data: rawpy.RawPy = rawpy.imread(str(p))
        data: NDArray[np.float64] = raw_data.postprocess(
            use_camera_wb=False,
            no_auto_bright=True,
            no_auto_scale=True,
            gamma=(1, 1),  #  This value is a key to "linear relation"
            output_bps=16,
        )
        if not args.color:
            data = rgb2gray(data)
        elif args.color.upper() in ["R", "G", "B"]:
            data = chose_single_color(data, args.color)
        elif "sum" in str(args.color).lower():
            data = rgb2sum(data)
        else:
            msg = "The --color option is invalid."
            raise RuntimeError(msg)

        data = crop(data)
        data = remove_cluster_spikes(data, diff_threshold=300)
        imageio.imsave(p.stem + ".tiff", data.astype("uint16"))
