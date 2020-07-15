# -*- coding: utf-8 -*-

import os

import numpy as np

try:
    import pes.splab as splab
except ImportError:
    import splab
#
try:
    import pes.arpes as arpes
except ImportError:
    import arpes
#


class TestARPES(object):
    def setup_method(self, method):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        self.splab041 = splab.load(datadir + "SPLab-041.xml")
        self.arpes041 = self.splab041.groups[0].regions[0].make_arpesmap()

    def test_axis(self):
        """Test for ARPES map axis"""
        np.testing.assert_allclose(
            np.array([0.0, 1.153846, 2.307692]),
            self.arpes041.second_axis[0:3],
            rtol=1e-06,
        )
        np.testing.assert_allclose(
            np.array([19.615385, 20.769231, 21.923077]),
            self.arpes041.angle_degs[-3:],
            rtol=1e-06,
        )
        assert self.arpes041.angle_degs[-1] == 21.9230769230769
        np.testing.assert_allclose(
            np.array([5.1 + i * 0.01 for i in range(211)]),
            self.splab041.groups[0].regions[0].energy_axis,
        )

    def test_angle_and_energy_shift(self):
        self.arpes041.angle_shift(4.0)
        np.testing.assert_allclose(
            np.array([4.0, 5.153846, 6.307692]),
            self.arpes041.angle_degs[0:3],
            rtol=1e-06,
        )
        self.arpes041.energy_shift(-3.0)
        np.testing.assert_allclose(
            np.array([2.1, 2.11, 2.12, 2.13]),
            self.arpes041.energy_axis[0:4],
            rtol=1e-06,
        )

    def test_angle_to_k(self):
        """Test for ARPESmap -> ARPESband method."""
        energymax = np.max(self.arpes041.energy_axis)
        energymin = np.min(self.arpes041.energy_axis)
        kmax = (
            0.512
            * np.sqrt(energymax)
            * np.sin(np.max(self.arpes041.second_axis) * np.pi / 180)
        )
        kmin = (
            0.512
            * np.sqrt(energymin)
            * np.sin(np.min(self.arpes041.angle_degs) * np.pi / 180)
        )
        assert kmax == 0.51293896353914326
        assert kmin == 0

    def test_ARPESband(self):
        """Test for ARPESband object."""
        band = self.arpes041.convert2band()
        assert band.k_axis[0] == 0
        np.testing.assert_array_almost_equal(band.k_axis[-1], 0.499212)

    # k = self.arpes041.angle_to_k()
