# -*- coding: utf-8 -*-

import os
from nose.tools import with_setup
from nose.tools import eq_
import rhk.rhksm4

class TestSM4(object):
    '''Class for test of rhksm4 module

    Use data3293FFT.sm4 in data directory
    '''
    def setup(self):
        datadir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
        data_file1 = datadir + 'data3293FFT.sm4'
        self.fft = rhk.rhksm4.SM4File(data_file1)


    @with_setup(setup=setup)
    def test_fileheader(self):
        eq_('STiMage 005.004 1\x00', self.fft.signature.decode('utf-16'))
        eq_(2, self.fft.pagecount)
        eq_(3, len(self.fft.children))
        
