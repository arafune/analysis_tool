#! /usr/bin/env python3
"""Convert to tiff image file from the LEED picture taken by EOS Kiss X5

Format of the output tiff file is:

    * No white balance added
    * No auto scale added
    * No auto bright added
    * 16 bit (The brightest is 65536.)

to evaluate numerically. """

import argparse
import pathlib
import imageio
import rawpy
import numpy as np


def crop(
    pic: np.ndarray[int], x: int = 890, y: int = 1974, side_length: int = 1800
) -> np.ndarray[int]:
    """Return cropping data of the gray scale

    Parameters
    -----------
    gray: numpy.ndarray
        grayscale data
    x: int
        x-point of the corner
    y: int
        y-point of the corner
    side_length: int
        the length of the square side

    Returns
    ----------
    numpy.ndarray
    """
    if pic.ndim == 2:
        return pic[x : x + side_length, y : y + side_length]
    elif pic.ndim == 3:
        return pic[x : x + side_length, y : y + side_length, :]


def rgb2gray(rgb: np.ndarray) -> np.ndarray:
    """Return Gray scale data.

    Use Matlab algorithm
    0.2989 * R + 0.5870 * G + 0.1140 * B

    Parameters
    -----------
    rgb: numpy.ndarray

    Returns
    ---------
    numpy.ndarray
    """
    return rgb[:, :, 0] * 0.2989 + rgb[:, :, 1] * 0.5870 + rgb[:, :, 2] * 0.1140


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
        data: np.ndarray = raw_data.postprocess(
            use_camera_wb=False, no_auto_bright=True, no_auto_scale=True, output_bps=16
        )
        if not args.color:
            data = rgb2gray(data)
        data = crop(data)
        if args.color:
            newfilename = p.stem + ".color.tiff"
        else:
            newfilename = p.stem + ".tiff"
        imageio.imsave(newfilename, data.astype("uint16"))
