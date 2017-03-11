# -*- coding: utf-8 -*-

import os
from nose.tools import ok_, eq_
from nose.tools import with_setup

import pes.splab as splab

class TestSPLab(object):
    def setup(self):
        datadir = os.path.abspath(os.path.dirname(__file__))+"/data/"
        self.splab041 = splab.splab(datadir+"SPLab-041.xml"

    @with_setup(setup=setup)
    def test_param(self):
        eq_("Region1", self.splab041.groups[0].regions[0].name)
        eq_(1,  self.splab041.groups[0].regions[0].param['num_1scan'])
