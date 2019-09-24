# -*- coding utf-8 -*-
"""Module for read data of QUADSTAR 32  (Q-mass system in Yoshinobu-san's lab).
"""

import struct
from datetime import datetime
from logging import DEBUG, Formatter, StreamHandler, getLogger

import numpy as np

LOGLEVEL = DEBUG
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

    """
    def __init__(self, fhandle):
        """Initialize (File load)."""
        sac_data = open(fhandle, "rb")
        sac_data.seek(100, 0)
        self.n_cyc = struct.unpack("@i", sac_data.read(4))[0]
        self.n_dbc = struct.unpack("@h", sac_data.read(2))[0]
        self.cycle_length = struct.unpack("@i", sac_data.read(4))[0]
        logger.debug('n_cyc: {}'.format(self.n_cyc))
        logger.debug('n_dbc: {}'.format(self.n_dbc))
        logger.debug('cycle_length {}'.format(self.cycle_length))
        sac_data.seek(194, 0)
        self.start_time = struct.unpack("@I", sac_data.read(4))[0]
        logger.debug('start time(unixtime): {}'.format(self.start_time))
        logger.debug('start time(UTC): {}'.format(
            datetime.fromtimestamp(self.start_time)))
        #
        for i in range(self.n_cyc):
            sac_data.seek(200 + i * 9, 0)
            self.cyc_type = struct.unpack("@b", sac_data.read(1))[0]
            logger.debug("cyc_type {}".format(self.cyc_type))
            self.hpos = struct.unpack("@i", sac_data.read(4))[0]
            logger.debug("hpos {}".format(self.hpos))
            self.dpos = struct.unpack("@i", sac_data.read(4))[0]
            logger.debug("dpos {}".format(self.dpos))
            if self.cyc_type == 17:
                break
        #
        sac_data.seek(self.hpos, 0)
        self.df = struct.unpack("@b", sac_data.read(1))[0]
        self.did = struct.unpack("@b", sac_data.read(1))[0]
        logger.debug('df, did: {0}, {1}'.format(self.df, self.did))

        sac_data.seek(self.hpos + 28, 0)
        self.sid = struct.unpack("@b", sac_data.read(1))[0]
        sac_data.seek(self.hpos + 123, 0)
        self.firstmass = struct.unpack("@i", sac_data.read(4))[0]
        self.scanwidth = struct.unpack("@h", sac_data.read(2))[0]
        logger.debug('1stMass, scanwidth: {0} {1}'.format(
            self.firstmass, self.scanwidth))
        self.n_m = struct.unpack("@i", sac_data.read(4))[0]
        logger.debug("number of measurements per mass {}".format(self.n_m))
        #
        sac_data.seek(self.dpos + 6, 0)
        self.anz = struct.unpack("@i", sac_data.read(4))[0]
        self.range = struct.unpack("@h", sac_data.read(2))[0]
        logger.debug("anz, range {0}, {1}".format(self.anz, self.range))
        #
        self.current = []
        sac_data.seek(self.dpos + 12, 0)
        for i in range(self.anz):
            self.current.append(struct.unpack("@f", sac_data.read(4))[0])


#            logger.debug('num of i: {}'.format(i))

    @property
    def mass_amu(self):
        """Return the axis-x."""
        return np.linspace(self.firstmass, self.firstmass + self.scanwidth,
                           self.anz)

if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    SM4 = SACObject(filename)
