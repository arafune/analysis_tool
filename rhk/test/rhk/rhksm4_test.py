# -*- coding: utf-8 -*-

import os
from nose.tools import with_setup
from nose.tools import eq_
from nose.tools import ok_
import rhk.rhksm4


class TestSM4(object):
    '''Class for test of rhksm4 module

    Use data3293FFT.sm4 in data directory
    '''
    def setup(self):
        datadir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
        #
        data_file1 = datadir + 'data3293FFT.sm4'
        self.fft = rhk.rhksm4.SM4File(data_file1)
        #
        data_file2 = datadir + 'Co_Ru0001_1300.SM4'
        data2 = open(data_file2, 'rb')
        self.co_ru = rhk.rhksm4.SM4File(data2)

    @with_setup(setup=setup)
    def test_fileheader(self):
        #
        eq_('STiMage 005.004 1\x00', self.fft.signature.decode('utf-16'))
        eq_(2, self.fft.pagecount)
        eq_(3, len(self.fft.children))
        #
        eq_('STiMage 005.004 1\x00', self.co_ru.signature.decode('utf-16'))
        eq_(6, self.co_ru.pagecount)
        eq_(3, len(self.co_ru.children))

    @with_setup(setup=setup)
    def test_PageIndexHeader(self):
        #
        pih = self.fft.children[0]
        eq_(1, pih.objtype)
        eq_('PageIndexHeader', pih.objname)
        eq_(2, pih.pagecount)
        eq_(1, len(pih.children))

    @with_setup(setup=setup)
    def test_PageIndexArray(self):
        #
        pia = self.fft.children[0].children[0]
        eq_(2, pia.objtype)
        eq_('PageIndexArray', pia.objname)
        eq_(2, len(pia.pages))
        eq_(0, len(pia.children))
        #
        pia2 = self.co_ru.children[0].children[0]
        eq_(2, pia2.objtype)

    @with_setup(setup=setup)
    def test_Page(self):
        #
        page = self.fft.children[0].children[0].pages[0]
        ok_(isinstance(page, rhk.rhksm4.RHKPage))
        eq_('image data', page.datatype_name)
        eq_('processed page', page.sourcetype_name)
        eq_(4, page.objcount)

    @with_setup(setup=setup)
    def test_PageHeader(self):
        #
        ph = self.fft.children[0].children[0].pages[0].children[0]
        ok_(isinstance(ph, rhk.rhksm4.RHKObject))
        #
        eq_('PageHeader', ph.objname)
        #
        eq_(180, ph.fieldsize)
        eq_(17, ph.strcount)
        eq_(6, ph.page)  # 6 means image FFT transform
        eq_(0, ph.datasubsource)
        eq_(0, ph.linetype)
        eq_(0, ph.x_coord)
        eq_(0, ph.y_coord)
        eq_(256, ph.x_size)
        eq_(256, ph.y_size)
        eq_(0, ph.image_type)
        eq_(1, ph.scan_dir)
        eq_(54301564, ph.group_id)
        eq_(262144, ph.data_size)  # 256 x 256 x 4 (4 is float bytes)
        eq_(180, ph.min_z_value)
        eq_(1407, ph.max_z_value)
        #  physical values
        eq_(-20000002.0, ph.x_scale)  # X physical units per pixel or bit
        eq_(-20000002.0, ph.y_scale)  # Y physical units per pixel or bit
        eq_(1.7287545688304817e-06, ph.z_scale)
        eq_(0, ph.xy_scale)
        #  offset
        eq_(0, ph.x_offset)
        eq_(0, ph.y_offset)
        eq_(0.0033952740486711264, ph.z_offset)
        #  Measurement conditions
        eq_(0.011718700639903545, ph.period)  # Period 0.011719 s
        eq_(0.16017913818359375, ph.bias)  # Bias 0.160179 V
        eq_(1.995468235094222e-09, ph.current)  # 2 nA
        eq_(0, ph.angle)
        #
        eq_(1, ph.colorinfocount)
        eq_(0, ph.grid_x_size)
        eq_(0, ph.grid_y_size)
        eq_(9, ph.objcount)

        eq_('StringData', ph.children[0].objname)
        eq_(5, ph.children[1].objtype)
        eq_(6, ph.children[2].objtype)
        eq_(0, ph.children[3].objtype)
        eq_(0, ph.children[4].objtype)
        eq_(9, ph.children[5].objtype)
        eq_(11, ph.children[6].objtype)
        eq_(0, ph.children[7].objtype)
        eq_(17, ph.children[8].objtype)

    @with_setup(setup=setup)
    def test_PageData(self):
        pd = self.fft.children[0].children[0].pages[0].children[1]
        ok_(isinstance(pd.data, tuple))
        eq_(256*256, len(pd.data))

    def test_StringData(self):
        stringdata =\
            self.fft.children[0].children[0].pages[0].children[0].children[0]
        eq_('FFT image', stringdata.strings[0])
        eq_('Page 14 of 26, 0.00 V', stringdata.strings[1])
        eq_('WTe2 4.78K  sens=50 mod=20mV 616Hz TC=3', stringdata.strings[2])
        eq_('', stringdata.strings[3])
        eq_('D:\\SPMdata\\20160421\\data3293FFT.sm4', stringdata.strings[4])
        eq_('04/22/16', stringdata.strings[5])
        eq_('11:01:44', stringdata.strings[6])
        eq_('m-1', stringdata.strings[7])
        eq_('m-1', stringdata.strings[8])
        eq_('V', stringdata.strings[9])
        for i in range(10, 13):
            eq_('', stringdata.strings[i])
        eq_('0256', stringdata.strings[13])
        eq_('337', stringdata.strings[14])
        eq_('', stringdata.strings[15])
        eq_('', stringdata.strings[16])

    def test_ThumbnailHeader(self):
        tnh = self.fft.children[0].children[0].pages[0].children[3]
        ok_(128, tnh.width)
        ok_(128, tnh.height)
#

    def test_PRMHeader(self):
        prmh = self.fft.children[2]
        eq_(3, len(prmh.header))
        eq_(1, prmh.header[0])
        eq_(67092, prmh.header[1])
        eq_(13521, prmh.header[2])
