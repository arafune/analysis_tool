# -*- coding utf-8 -*-
"""Module for read data of QUADSTAR 32  (Q-mass system in Yoshinobu-san's lab).
"""

import struct

import numpy as np


class SACObject:
    """Class for SAC data file.

    Attributes
    -------------
    n_cyc: int
       Number of cycles

    """
    def __init__(self, fhandle):
        """Initialize (File load)."""
        sac_data = open(fhandle, 'rb')
        sac_data.seek(100, 0)
        self.n_cyc = struct.unpack('@i', sac_data.read(4))[0]
        self.n_dbc = struct.unpack('@h', sac_data.read(2))[0]
        self.cycle_length = struct.unpack('@i', sac_data.read(4))[0]
        #
        sac_data.seek(194, 0)
        self.start_time = struct.unpack('@I', sac_data.read(4))[0]
        #
        for i in range(self.n_cyc):
            sac_data.seek(200 + i * 9, 0)
            self.cyc_type = struct.unpack("@b", sac_data.read(1))[0]
            self.hpos = struct.unpack("@i", sac_data.read(4))[0]
            self.dpos = struct.unpack("@i", sac_data.read(4))[0]
        #
        sac_data.seek(self.hpos, 0)
        self.df = struct.unpack("@b", sac_data.read(1))[0]
        self.did = struct.unpack("@b", sac_data.read(1))[0]
        sac_data.seek(self.hpos + 28, 0)
        self.sid = struct.unpack("@b", sac_data.read(1))[0]
        sac_data.seek(self.hpos + 123, 0)
        self.firstmass = struct.unpack("@i", sac_data.read(4))[0]
        self.scanwidth = struct.unpack("@h", sac_data.read(2))[0]
        self.n_m = struct.unpack("@i", sac_data.read(4))[0]
        #
        sac_data.seek(self.dpos + 6, 0)
        self.anz = struct.unpack("@i", sac_data.read(4))[0]
        self.range = struct.unpack("@h", sac_data.read(2))[0]
        #
        self.current = []
        sac_data.seek(self.dpos + 12, 0)
        for i in range(self.anz):
            self.current.append(struct.unpack("@f", sac_data.read(4))[0])

    @property
    def mass_amu(self):
        """Return the axis-x."""
        return np.linspace(self.firstmass, self.firstmass + self.scanwidth,
                           self.anz)
