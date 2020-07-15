# -*- coding: utf-8 -*-
"""Module to analyze and show SPECS calib1d data."""

from typing import Union, Optional, List
import numpy as np
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


class Calib1d:
    """Class for .calib1d file

    Attributes
    --------------
    file_name: str
        file name for read
    """

    SL_Version: str = "4.57.1-r83491"
    SL_Build_Date: str = "2019-06-19 10:39:02 UTC"

    def __init__(self, file_name: Union[str, Path, None] = None) -> None:
        """Initialization.

        Parameters
        ------------
        file_name: str
            calib1d data file name.  Suffix is .calib1d.
        """
        self.positions: Union[List[float], np.ndarray] = []
        self.shifts: Union[List[float], np.ndarray] = []
        self.header: OrderedDict[str, Optional[str]] = OrderedDict()
        if file_name is None:
            self.header = {}
            self.positions = np.array([])
            self.shifts = np.array([])
        else:
            with open(file_name, "r") as fileread:
                for line in fileread:
                    if line[0] == "#":
                        if "##" in line:
                            line = "#\n" + line
                        self._read_header(line)
                    else:
                        data: List[str] = line.split(" ")
                        self.positions.append(float(data[0]))
                        self.shifts.append(float(data[1]))
                self.positions = np.array(self.positions)
                self.shifts = np.array(self.shifts)

    def _read_header(self, line: str) -> None:
        """Read header.

        Attributes
        -------------
        line: str
            line for read, begin with "#"
        """
        if "=" in line:
            item, value = line.split("=")
            self.header[item] = value
        else:
            self.header[line] = None

    def write_header(self) -> str:
        """Build header."""
        output_header: str = ""
        self.header["# Creation Date "] = ' "{}"\n'.format(
            datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S UTC")
        )
        for k, v in self.header.items():
            if v is None:
                output_header += k
            else:
                output_header += k + "=" + v
        return output_header

    def comment(self, text_str: str) -> None:
        """Add comment in header

        Attributes
        -----------
        text_str: str
            string for comment
        """
        self.header["# Comment       "] = ' "{}"\n'.format(text_str)

    def save(self, filename: str) -> None:
        with open(filename, mode="w") as f:
            f.write(self.write_header())
            for p, s in zip(self.positions, self.shifts):
                f.write("{:.5f} {:.7f} 1\n".format(p, s))

    def linearlization(self) -> None:
        """Correct the calibration by linear function.

        The calibration file is not linear file.
        This deviation from the linear function may be due to the fitting process,
        which depends on the spectrum used for calibration.
        By using this method, the calibration data becomes strict linear function.
        """
        func = np.poly1d(np.polyfit(self.positions, self.shifts, 1))
        self.shifts = func(self.positions)
