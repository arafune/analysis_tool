#!/usr/bin/env python
"""Test for SAC class."""

import os

import numpy as np

from qmass import sac


class Test_SAC_file:
    """Class for qmas.sac.SACObject."""

    def setup_method(self, method):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        datafile = datadir + "0904.SAC"
        self.sac = sac.SACObject(datafile)

    def test_parameters(self):
        """Check read parameters."""
        assert self.sac.n_cyc == 1
        assert self.sac.start_time == 1567616602
        assert self.sac.n_dbc == 2
        assert self.sac.cycle_length == 6412
        assert self.sac.cyc_type == 15
        assert self.sac.hpos == 218
        assert self.sac.dpos == 380
        assert self.sac.df == 8
        assert self.sac.did == 6
        assert self.sac.sid == 0
        assert self.sac.firstmass == 0
        assert self.sac.scanwidth == 50
        assert self.sac.n_m == 32  # number of measured value per pass
        assert self.sac.anz == 1600  # number pof points
        assert self.sac.range == -8
        #
        np.testing.assert_almost_equal(self.sac.current[0], 2.11444e-11)
        np.testing.assert_almost_equal(self.sac.current[-1], 3.35983e-11)
