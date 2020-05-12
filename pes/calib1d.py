# -*- coding: utf-8 -*-
"""Module to analyze and show SPECS calib1d data."""

import numpy as np
from scipy import interpolate


class Calib1d:
    """Class for .calib1d file
    
    Attributes
    --------------
    
    """

    def __init__(seflf, file_name=None):
        """Initialization.
        
        Parameters
        ------------
        file_name: str
            calib1d data file name.  Suffix is .calib1d.
        """

        data = []
