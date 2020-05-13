# -*- coding: utf-8 -*-
"""Module to analyze and show SPECS calib1d data."""

import numpy as np
from collections import OrderedDict
from datetime import datetime
from scipy import interpolate


class Calib1d:
    """Class for .calib1d file
    
    Attributes
    --------------
    
    """

    SL_Version = "4.57.1-r83491"
    SL_Build_Date = "2019-06-19 10:39:02 UTC"

    def __init__(self, file_name=None):
        """Initialization.
        
        Parameters
        ------------
        file_name: str
            calib1d data file name.  Suffix is .calib1d.
        """
        self.positions = []
        self.shifts = []
        self.header = OrderedDict()
        if file_name is None:
            self.creation_data = ""
            self.sl_version = ""
            self.sl_build_data = ""
            self.source = ""
            self.Comment = ""
            #
            self.lensmode = ""
            self.slit = ""
            self.analyzerconfig = ""
        else:
            with open(file_name, "r") as fileread:
                for line in fileread:
                    if line[0] == "#":
                        self.read_header(line)
                    else:
                        data = line.split(" ")
                        self.positions.append(float(data[0]))
                        self.shifts.append(float(data[1]))
                self.positions = np.array(self.positions)
                self.shifts = np.array(self.shifts)

    def read_header(self, line):
        """Read header."""
        if "=" in line:
            item, value = line.split("=")
            self.header[item] = value
        else:
            self.header[line] = None

    def write_header(self):
        """Build header."""
        self.header["# Creation Date "] = ' "{}"'.format(
            datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S UTC")
        )
        for k, v in self.header.items():
            if v is None:
                print(k)
            else:
                v.strip()
                print(k + "=" + v)

    def save(self, filename):
        pass
