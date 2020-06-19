# -*- coding: utf-8 -*-

import os

import numpy as np
from nose.tools import eq_, ok_, with_setup

try:
    import pes.splab as splab
except ImportError:
    import splab


class TestSPLab(object):
    def setup(self):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        self.splab041 = splab.load(datadir + "SPLab-041.xml")

    @with_setup(setup=setup)
    def test_param(self):
        eq_("Region1", self.splab041.groups[0].regions[0].name)
        eq_(1, self.splab041.groups[0].regions[0].param['num_scans'])
        eq_(1, self.splab041.groups[0].regions[0].param['dwell_time'])
        eq_('FixedAnalyzerTransmission',
            self.splab041.groups[0].regions[0].param['scan_mode'])
        eq_(1, self.splab041.groups[0].regions[0].param['pass_energy'])
        eq_(4.414,
            self.splab041.groups[0].regions[0].param['effective_workfunction'])
        eq_(1350, self.splab041.groups[0].regions[0].param['detector_voltage'])
        eq_(0.01, self.splab041.groups[0].regions[0].param['scan_delta'])
        eq_(5.092,
            self.splab041.groups[0].regions[0].param['excitation_energy'])
        eq_(5.1, self.splab041.groups[0].regions[0].param['kinetic_energy'])
        eq_((8, 8), self.splab041.groups[0].regions[0].mcd_head_tail)

    @with_setup(setup=setup)
    def test_analyser_info(self):
        eq_('PHOIBOS HSA3500 CCD 100 R5[HWType 30:13] CCD',
            self.splab041.groups[0].regions[0].analyzer_info['name'])
        np.testing.assert_allclose(
            np.array([[-16.6023, -0.0847422, 1], [-15.2091, -0.0770081, 1],
                      [-13.8159, -0.0699468, 1], [-12.4227, -0.0628961, 1],
                      [-11.0295, -0.0566889, 1], [-9.6363, -0.0497265, 1],
                      [-8.2431, -0.0429213, 1], [-6.8499, -0.0358507, 1],
                      [-5.4567, -0.0286102, 1], [-4.0635, -0.0220417, 1],
                      [-2.6703, -0.0147662, 1], [-1.2771, -0.00820503, 1],
                      [0.1161, -0.00168055, 1], [1.5093, 0.00614424, 1],
                      [2.9025, 0.0130663, 1], [4.2957, 0.0194439, 1],
                      [5.6889, 0.0263788, 1], [7.0821, 0.0329499, 1],
                      [8.4753, 0.0405154, 1], [9.8685, 0.0486007, 1],
                      [11.2617, 0.0547919, 1], [12.6549, 0.0627039, 1],
                      [14.0481, 0.0698935, 1], [15.4413, 0.0763826, 1]]),
            self.splab041.groups[0].regions[0].analyzer_info['Detector'])

    @with_setup(setup=setup)
    def test_mcd_head_tail(self):
        eq_(self.splab041.groups[0].regions[0].mcd_head_tail[0], 8)
        eq_(self.splab041.groups[0].regions[0].mcd_head_tail[1], 8)

    @with_setup(setup=setup)
    def test_energy_axis(self):
        """Test for energy axis including channel separated energy axis."""
        np.testing.assert_allclose(
            np.array([5.1, 5.11, 5.12, 5.13]),
            self.splab041.groups[0].regions[0].energy_axis[0:4])
        np.testing.assert_allclose(
            np.array([5.1 + i * 0.01 for i in range(211)]),
            self.splab041.groups[0].regions[0].energy_axis)
        np.testing.assert_allclose(
            np.array([4.935258, 4.945258, 4.955258, 4.965258, 4.975258]),
            self.splab041.groups[0].regions[0].energy_axis_ch[0][0:5])
