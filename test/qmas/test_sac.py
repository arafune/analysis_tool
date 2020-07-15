#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test for SAC class"""

import os

import numpy as np

import qmass.sac as sac


class Test_SAC_file:
    """Class for qmas.sac.SACObject"""

    def setup_method(self, method):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        datafile = datadir + "0904.SAC"
        self.sac = sac.SACObject(datafile)

    def test_parameters(self):
        """Check read parameters.
        """
        assert 1 == self.sac.n_cyc
        assert 1567616602 == self.sac.start_time
        assert 2 == self.sac.n_dbc
        assert 6412 == self.sac.cycle_length
        assert 15 == self.sac.cyc_type
        assert 218 == self.sac.hpos
        assert 380 == self.sac.dpos
        assert 8 == self.sac.df
        assert 6 == self.sac.did
        assert 0 == self.sac.sid
        assert 0 == self.sac.firstmass
        assert 50 == self.sac.scanwidth
        assert 32 == self.sac.n_m  # number of measured value per pass
        assert 1600 == self.sac.anz  # number pof points
        assert -8 == self.sac.range
        #
        np.testing.assert_almost_equal(self.sac.current[0], 2.11444e-11)
        np.testing.assert_almost_equal(self.sac.current[-1], 3.35983e-11)
