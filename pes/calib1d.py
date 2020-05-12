# -*- coding: utf-8 -*-
"""Module to analyze and show SPECS calib1d data."""

import numpy as np
from scipy import interpolate


class Calib1d:
    """Class for .calib1d file
    
    Attributes
    --------------
    
    """

    def __init__(self, file_name=None):
        """Initialization.
        
        Parameters
        ------------
        file_name: str
            calib1d data file name.  Suffix is .calib1d.
        """
        self.positions = []
        self.shifts = []
        self.header = []
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
                        self.header.append(line)
                    else:
                        line.strip()
                        data = line.split(" ")
                        self.positions.append(float(data[0]))
                        self.shifts.append(float(data[1]))
                self.positions = np.array(self.positions)
                self.shifts = np.array(self.shifts)
