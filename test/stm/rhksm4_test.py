# -*- coding: utf-8 -*-

import os

import stm.rhksm4 as rhksm4


class TestSM4(object):
    """Class for test of rhksm4 module

    Use data3293FFT.sm4 in data directory
    """

    def setup_method(self):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        #
        data_file1 = datadir + "data3293FFT.sm4"
        self.fft = rhksm4.SM4File(data_file1)
        #
        data_file2 = datadir + "Co_Ru0001_1300.SM4"
        data2 = open(data_file2, "rb")
        self.co_ru = rhksm4.SM4File(data2)

    def test_fileheader(self):
        #
        assert "STiMage 005.004 1\x00" == self.fft.signature.decode("utf-16")
        assert 2 == self.fft.pagecount
        assert 3 == len(self.fft.children)
        #
        assert "STiMage 005.004 1\x00" == self.co_ru.signature.decode("utf-16")
        assert 6 == self.co_ru.pagecount
        assert 3 == len(self.co_ru.children)

    def test_PageIndexHeader(self):
        #
        pih = self.fft.children[0]
        assert 1 == pih.objtype
        assert "PageIndexHeader" == pih.objname
        assert 2 == pih.pagecount
        assert 1 == len(pih.children)

    def test_PageIndexArray(self):
        #
        pia = self.fft.children[0].children[0]
        assert 2 == pia.objtype
        assert "PageIndexArray" == pia.objname
        assert 2 == len(pia.pages)
        assert 0 == len(pia.children)
        #
        pia2 = self.co_ru.children[0].children[0]
        assert 2 == pia2.objtype

    def test_Page(self):
        #
        page = self.fft.children[0].children[0].pages[0]
        isinstance(page, rhksm4.RHKPage)
        assert "image data" == page.datatype_name
        assert "processed page" == page.sourcetype_name
        assert 4 == page.objcount

    def test_PageHeader(self):
        #
        ph = self.fft.children[0].children[0].pages[0].children[0]
        isinstance(ph, rhksm4.RHKObject)
        #
        assert "PageHeader" == ph.objname
        #
        assert 180 == ph.fieldsize
        assert 17 == ph.strcount
        assert 6 == ph.page  # 6 means image FFT transform
        assert 0 == ph.datasubsource
        assert 0 == ph.linetype
        assert 0 == ph.x_coord
        assert 0 == ph.y_coord
        assert 256 == ph.x_size
        assert 256 == ph.y_size
        assert 0 == ph.image_type
        assert 1 == ph.scan_dir
        assert 54301564 == ph.group_id
        assert 262144 == ph.data_size  # 256 x 256 x 4 (4 is float bytes)
        assert 180 == ph.min_z_value
        assert 1407 == ph.max_z_value
        #  physical values
        assert -20000002.0 == ph.x_scale  # X physical units per pixel or bit
        assert -20000002.0 == ph.y_scale  # Y physical units per pixel or bit
        assert 1.7287545688304817e-06 == ph.z_scale
        assert 0 == ph.xy_scale
        #  offset
        assert 0 == ph.x_offset
        assert 0 == ph.y_offset
        assert 0.0033952740486711264 == ph.z_offset
        #  Measurement conditions
        assert 0.011718700639903545 == ph.period  # Period 0.011719 s
        assert 0.16017913818359375 == ph.bias  # Bias 0.160179 V
        assert 1.995468235094222e-09 == ph.current  # 2 nA
        assert 0 == ph.angle
        #
        assert 1 == ph.colorinfocount
        assert 0 == ph.grid_x_size
        assert 0 == ph.grid_y_size
        assert 9 == ph.objcount

        assert "StringData" == ph.children[0].objname
        assert 5 == ph.children[1].objtype
        assert 6 == ph.children[2].objtype
        assert 0 == ph.children[3].objtype
        assert 0 == ph.children[4].objtype
        assert 9 == ph.children[5].objtype
        assert 11 == ph.children[6].objtype
        assert 0 == ph.children[7].objtype
        assert 17 == ph.children[8].objtype

    def test_PageData(self):
        pd = self.fft.children[0].children[0].pages[0].children[1]
        isinstance(pd.data, tuple)
        assert 256 * 256 == len(pd.data)

    def test_StringData(self):
        stringdata = self.fft.children[0].children[0].pages[0].children[0].children[0]
        assert "FFT image" == stringdata.strings[0]
        assert "Page 14 of 26, 0.00 V" == stringdata.strings[1]
        assert "WTe2 4.78K  sens=50 mod=20mV 616Hz TC=3" == stringdata.strings[2]
        assert "" == stringdata.strings[3]
        assert "D:\\SPMdata\\20160421\\data3293FFT.sm4" == stringdata.strings[4]
        assert "04/22/16" == stringdata.strings[5]
        assert "11:01:44" == stringdata.strings[6]
        assert "m-1" == stringdata.strings[7]
        assert "m-1" == stringdata.strings[8]
        assert "V" == stringdata.strings[9]
        for i in range(10, 13):
            assert "" == stringdata.strings[i]
        assert "0256" == stringdata.strings[13]
        assert "337" == stringdata.strings[14]
        assert "" == stringdata.strings[15]
        assert "" == stringdata.strings[16]

    def test_ThumbnailHeader(self):
        tnh = self.fft.children[0].children[0].pages[0].children[3]
        assert 128 == tnh.width
        assert 128 == tnh.height

    #

    def test_PRMHeader(self):
        prmh = self.fft.children[2]
        assert 3 == len(prmh.header)
        assert 1 == prmh.header[0]
        assert 67092 == prmh.header[1]
        assert 13521 == prmh.header[2]
