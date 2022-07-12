# -*- coding utf-8 -*-
"""Module for read data of QUADSTAR 32  (Q-mass system in Yoshinobu-san's lab).
"""

import struct
from datetime import datetime
from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger

import numpy as np

LOGLEVEL = INFO
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


class SACObject:
    """Class for SAC data file.

    Attributes
    -------------
    n_cyc: int
       Number of cycles
    scan_width: int
       scan width
    first_mass: float
       first mass
    mass_start: float
       mass start (Essentially same as first mass?)
    mass_end: float
       mass end
    start_time: int
       Unix time for record
    n_m: int
       number of measurements for each mass
    data: 2D-array
       mass data
    mass_amu: 1D-array
       X-axis data for QMS
    """

    def __init__(self, fhandle: str) -> None:
        """Initialize (File load)."""
        sac_data = open(fhandle, "rb")
        sac_data.seek(100, 0)
        self.n_cyc = struct.unpack("@i", sac_data.read(4))[0]
        logger.debug("n_cyc: {}".format(self.n_cyc))
        sac_data.seek(345, 0)
        self.scan_width = struct.unpack("@h", sac_data.read(2))[0]
        logger.debug("scan_width: {}".format(self.scan_width))
        sac_data.seek(341, 0)
        self.firstmass = struct.unpack("@f", sac_data.read(4))[0]
        sac_data.seek(348, 0)
        self.mass_start = struct.unpack("@f", sac_data.read(4))[0]
        self.mass_end = struct.unpack("@f", sac_data.read(4))[0]
        logger.debug(
            "first-, start-, end-mass: {0}, {1}, {2}".format(
                self.firstmass, self.mass_start, self.mass_end
            )
        )
        sac_data.seek(194, 0)
        self.start_time = struct.unpack("@I", sac_data.read(4))[0]
        logger.debug("start_time: {0}".format(self.start_time))
        sac_data.seek(347, 0)
        self.n_m = struct.unpack("@B", sac_data.read(1))[
            0
        ]  # number of measurements for each mass
        logger.debug("N of measurements for each mass: {0}".format(self.n_m))
        self.data = []
        #
        DATA_START_ADD = 392
        sac_data.seek(DATA_START_ADD - 12, 0)
        total_n_points = round(self.scan_width * self.n_m)
        for cycle in range(self.n_cyc):
            sac_data.seek(12, 1)
            tmp = []
            for mass_index in range(total_n_points):
                tmp.append(struct.unpack("@f", sac_data.read(4))[0])
            self.data.append(tmp)
        logger.debug("len of data {}".format(len(self.data)))
        self.mass_amu = np.linspace(
            self.mass_start,
            self.mass_start + self.scan_width,
            total_n_points,
            endpoint=False,
        )
        logger.debug("First mass value {}".format(self.mass_amu[0]))
        logger.debug("Last mass value {}".format(self.mass_amu[-1]))


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    SM4 = SACObject(filename)
