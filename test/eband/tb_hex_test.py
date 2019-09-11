#/usr/bin/env python3
"""Unit test for tb_hex_test."""

import os

import numpy as np
from nose.tools import eq_, ok_, with_setup

import eband.tb_hex as tb_hex


class Test_TightBinding(object):
    def setup(self):
        self.testhex0 = tb_hex.Band()

    @with_setup(setup=setup)
    def test_Band(self):
        length_kg = tb_hex.distance(self.testhex0.kg)
        np.testing.assert_array_almost_equal(length_kg[-1], 2.7925268031909276)
        np.testing.assert_equal(self.testhex0.kg[0][-1], 0)
        np.testing.assert_equal(self.testhex0.energy(0, 0),
                                (6.16227766016838, -0.16227766016837952))
