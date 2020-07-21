# -*- coding: utf-8 -*-
""".. py:module:: qpi

Module to extract the line profile data about QPI results.
"""

import os.path
from __future__ import annotations
import numpy as np
from typing import Sequence


class QPI:
    """Class for QPI data.

    Attributes
    ------------
    data: tuple, list, numpy.ndarray
        1D or 2D matrix data.  The size of data should be n**2.
    physical_size: float
        The length of the horizontal line.
    bias: float
        The bias voltage in V unit.
    current: float
        The tunneling current in nA unit.

    """

    def __init__(
        self,
        data: Sequence[float],
        physical_size: float = 0,
        bias: float = 0,
        current: float = 0,
        dataname: str = "",
    ) -> None:
        """Initialization."""
        self.data: np.ndarray = np.array(data, dtype=np.float_)
        self.pixels: int
        if self.data.ndim == 1:
            self.pixels = int(np.sqrt(self.data.shape[0]))
            self.data = self.data.reshape(self.pixels, self.pixels)
        elif self.data.ndim == 2 and self.data.shape[0] == self.data.shape[1]:
            self.pixels = self.data.shape[0]
        else:
            raise ValueError("Data mismatch!")
        if physical_size == 0:
            self.physical_size = self.data.shape[0]
        else:
            self.physical_size = physical_size
        self.bias = bias
        self.current = current
        self.dataname = dataname

    def cross_section_by_degree(self, angle_deg: float) -> np.ndarray:
        """Return the intensities along the line tilted by the angle.

        Parameters
        ----------
        angle_deg: float
            Cutting angle by degrees

        """
        degree: float = np.pi / 180.0
        if -1.0 < np.tan(angle_deg * degree) <= 1.0:
            position_pixel = [
                (x, self.ypixel(x, angle_deg)) for x in range(self.pixels)
            ]
        else:
            position_pixel = [
                (
                    int(
                        (y - self.pixels / 2.0) / np.tan(angle_deg * degree)
                        + self.pixels / 2.0
                    ),
                    y,
                )
                for y in range(self.pixels)
            ]
        return np.array([self.data[pos] for pos in position_pixel])

    def ypixel(self, x: float, angle_deg: float) -> int:
        """Calculate y pixel with quantization-error correction.

        Parameters
        ----------
            x: float

            angle_deg: float
                Cutting angle by degrees

        """
        degree: float = np.pi / 180.0
        y = int(
            np.tan(angle_deg * degree) * (x - self.pixels / 2.0) + self.pixels / 2.0
        )
        if y >= self.pixels:
            y = self.pixels - 1
        elif y < 0:
            y = 0
        return y

    def physical_axis(self, angle_deg: float) -> np.ndarray:
        """Calculate k-value along the line tilted by the angle.

        Parameters
        ----------
        angle_deg: float
            Cutting angle by degrees

        """
        degree: float = np.pi / 180.0
        if -1.0 <= np.tan(angle_deg * degree) <= 1.0:
            return np.linspace(
                -self.physical_size / 2.0 * np.abs(1 / np.cos(angle_deg * degree)),
                self.physical_size / 2.0 * np.abs(1 / np.cos(angle_deg * degree)),
                self.pixels,
            )
        else:
            return np.linspace(
                -self.physical_size / 2.0 * np.abs(1 / np.sin(angle_deg * degree)),
                self.physical_size / 2.0 * np.abs(1 / np.sin(angle_deg * degree)),
                self.pixels,
            )


def qpidataload(filename: str) -> QPI:
    """Loader for the file converted from SM4.

    Parameters
    ----------
    filename: str
        The file name of SM4-file.

    Returns
    -------
        QPI: QPI object

    """
    dataname = os.path.splitext(filename)[0]
    thefile = open(filename)
    data = []
    with thefile:
        [next(thefile) for i in range(4)]
        tmp = next(thefile)
        bias, bias_unit, current = (
            float(tmp.split()[3]),
            tmp.split()[4],
            float(tmp.split()[6]),
        )
        if bias_unit in "mV,":
            bias = float(bias) / 1000
        [next(thefile) for i in range(2)]
        xdim = float(next(thefile).split()[2])
        [next(thefile) for i in range(5)]
        for line in thefile:
            data.append(line.split()[1:])
    return QPI(data, physical_size=xdim, bias=bias, current=current, dataname=dataname)


def anglestring(angle: float) -> str:
    """Return the angle string with 'm' when the angle is negative.

    Parameters
    -----------
        angle: float
            The angle.

    Returns
    ---------
        str
            When the angle is negative, return 'm'+abs(angle).

"""
    if angle < 0:
        return "m" + str(abs(angle))
    else:
        return str(angle)
