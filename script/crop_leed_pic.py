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
    -----------
    rgb: NDArray

    Returns
    ---------
    NDArray
    """
    return rgb[:, :, 0] * 0.2989 + rgb[:, :, 1] * 0.5870 + rgb[:, :, 2] * 0.1140
    # return rgb[:, :, 1]  # Take the green signal


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("CR2file", help="CR2 file of the LEED picture", nargs="*")
    parse.add_argument(
        "--color",
        "-c",
        action="store_true",
        default=False,
        help="Keep color information.",
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
        data = crop(data)
        if args.color:
            newfilename = p.stem + ".color.tiff"
        else:
            newfilename = p.stem + ".tiff"
        imageio.imsave(newfilename, data.astype("uint16"))
