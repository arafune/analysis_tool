import os
from pathlib import Path

from stm import rhksm4


class TestSM4:
    """Class for test of rhksm4 module.

    Use data3293FFT.sm4 in data directory
    """

    def setup_method(self):
        datadir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
        #
        data_file1 = datadir + "data3293FFT.sm4"
        self.fft = rhksm4.SM4File(data_file1)
        #
        data_file2 = datadir + "Co_Ru0001_1300.SM4"
        data2 = Path(data_file2).open("rb")
        self.co_ru = rhksm4.SM4File(data2)

    def test_fileheader(self):
        #
        assert self.fft.signature.decode("utf-16") == "STiMage 005.004 1\x00"
        assert self.fft.pagecount == 2
        assert len(self.fft.children) == 3
        #
        assert self.co_ru.signature.decode("utf-16") == "STiMage 005.004 1\x00"
        assert self.co_ru.pagecount == 6
        assert len(self.co_ru.children) == 3

    def test_PageIndexHeader(self):
        #
        pih = self.fft.children[0]
        assert pih.objtype == 1
        assert pih.objname == "PageIndexHeader"
        assert pih.pagecount == 2
        assert len(pih.children) == 1

    def test_PageIndexArray(self):
        #
        pia = self.fft.children[0].children[0]
        assert pia.objtype == 2
        assert pia.objname == "PageIndexArray"
        assert len(pia.pages) == 2
        assert len(pia.children) == 0
        #
        pia2 = self.co_ru.children[0].children[0]
        assert pia2.objtype == 2

    def test_Page(self):
        #
        page = self.fft.children[0].children[0].pages[0]
        isinstance(page, rhksm4.RHKPage)
        assert page.datatype_name == "image data"
        assert page.sourcetype_name == "processed page"
        assert page.objcount == 4

    def test_PageHeader(self):
        #
        ph = self.fft.children[0].children[0].pages[0].children[0]
        isinstance(ph, rhksm4.RHKObject)
        #
        assert ph.objname == "PageHeader"
        #
        assert ph.fieldsize == 180
        assert ph.strcount == 17
        assert ph.page == 6  # 6 means image FFT transform
        assert ph.datasubsource == 0
        assert ph.linetype == 0
        assert ph.x_coord == 0
        assert ph.y_coord == 0
        assert ph.x_size == 256
        assert ph.y_size == 256
        assert ph.image_type == 0
        assert ph.scan_dir == 1
        assert ph.group_id == 54301564
        assert ph.data_size == 262144  # 256 x 256 x 4 (4 is float bytes)
        assert ph.min_z_value == 180
        assert ph.max_z_value == 1407
        #  physical values
        assert ph.x_scale == -20000002.0  # X physical units per pixel or bit
        assert ph.y_scale == -20000002.0  # Y physical units per pixel or bit
        assert ph.z_scale == 1.7287545688304817e-06
        assert ph.xy_scale == 0
        #  offset
        assert ph.x_offset == 0
        assert ph.y_offset == 0
        assert ph.z_offset == 0.0033952740486711264
        #  Measurement conditions
        assert ph.period == 0.011718700639903545  # Period 0.011719 s
        assert ph.bias == 0.16017913818359375  # Bias 0.160179 V
        assert ph.current == 1.995468235094222e-09  # 2 nA
        assert ph.angle == 0
        #
        assert ph.colorinfocount == 1
        assert ph.grid_x_size == 0
        assert ph.grid_y_size == 0
        assert ph.objcount == 9

        assert ph.children[0].objname == "StringData"
        assert ph.children[1].objtype == 5
        assert ph.children[2].objtype == 6
        assert ph.children[3].objtype == 0
        assert ph.children[4].objtype == 0
        assert ph.children[5].objtype == 9
        assert ph.children[6].objtype == 11
        assert ph.children[7].objtype == 0
        assert ph.children[8].objtype == 17

    def test_PageData(self):
        pd = self.fft.children[0].children[0].pages[0].children[1]
        isinstance(pd.data, tuple)
        assert 256 * 256 == len(pd.data)

    def test_StringData(self):
        stringdata = self.fft.children[0].children[0].pages[0].children[0].children[0]
        assert stringdata.strings[0] == "FFT image"
        assert stringdata.strings[1] == "Page 14 of 26, 0.00 V"
        assert stringdata.strings[2] == "WTe2 4.78K  sens=50 mod=20mV 616Hz TC=3"
        assert stringdata.strings[3] == ""
        assert stringdata.strings[4] == "D:\\SPMdata\\20160421\\data3293FFT.sm4"
        assert stringdata.strings[5] == "04/22/16"
        assert stringdata.strings[6] == "11:01:44"
        assert stringdata.strings[7] == "m-1"
        assert stringdata.strings[8] == "m-1"
        assert stringdata.strings[9] == "V"
        for i in range(10, 13):
            assert stringdata.strings[i] == ""
        assert stringdata.strings[13] == "0256"
        assert stringdata.strings[14] == "337"
        assert stringdata.strings[15] == ""
        assert stringdata.strings[16] == ""

    def test_ThumbnailHeader(self):
        tnh = self.fft.children[0].children[0].pages[0].children[3]
        assert tnh.width == 128
        assert tnh.height == 128

    #

    def test_PRMHeader(self):
        prmh = self.fft.children[2]
        assert len(prmh.header) == 3
        assert prmh.header[0] == 1
        assert prmh.header[1] == 67092
        assert prmh.header[2] == 13521
