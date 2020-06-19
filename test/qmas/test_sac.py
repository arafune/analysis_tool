#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test for SAC class"""

import os

import numpy as np
from nose.tools import assert_almost_equal, eq_, ok_, with_setup

import qmass.sac as sac


class Test_SAC_file():
    """Class for qmas.sac.SACObject"""
    def setup(self):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        datafile = datadir + '0904.SAC'
        self.sac = sac.SACObject(datafile)

    @with_setup(setup=setup)
    def test_parameters(self):
        """Check read parameters.
        """
        eq_(1, self.sac.n_cyc)
        eq_(1567616602, self.sac.start_time)
        eq_(2, self.sac.n_dbc)
        eq_(6412, self.sac.cycle_length)
        eq_(15, self.sac.cyc_type)
        eq_(218, self.sac.hpos)
        eq_(380, self.sac.dpos)
        eq_(8, self.sac.df)
        eq_(6, self.sac.did)
        eq_(0, self.sac.sid)
        eq_(0, self.sac.firstmass)
        eq_(50, self.sac.scanwidth)
        eq_(32, self.sac.n_m)  # number of measured value per pass
        eq_(1600, self.sac.anz)  # number pof points
        eq_(-8, self.sac.range)
        #
        np.testing.assert_almost_equal(self.sac.current[0], 2.11444E-11)
        np.testing.assert_almost_equal(self.sac.current[-1], 3.35983E-11)
