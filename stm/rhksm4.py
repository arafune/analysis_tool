# -*- coding: utf-8 -*-
""".. py:module:: rhksm4

Module to read the proprietary files SM4 from RHK technology

For writing the code I used some ideas from the Gwyddion project
(http://gwyddion.net/) where I found rhk-sm4.c. Some of variable names
are followed from it.
"""

import io
import struct
from types import MethodType


class ExtStruct(struct.Struct):
    """.. py:class:: ExtStruct()

    Helper class to treat pack/unpack smoothly"""

    def __init__(self, fmt):
        super().__init__(fmt)

    def unpack_from_file(self, fhandle):
        """.. py:method:: unpack_from_file(fhandle)

        Helper function to unpack from file

        Parameters
        ----------
        fhandle: io.IOBase
            The file handle
        """
        return self.unpack(fhandle.read(self.size))


def get_objects_from_list(fhandle, n, parent):
    """.. py:function:: get_objects_from_list(fhandle, n, parent)

    Parameters
    ------------
    fhandle: io.IOBase
       The file handle
    n: int
       Number of objects to read
    parent: object
       Parent Object

    Returns
    ----------
    list
       Contains RHKObject
"""
    return [RHKObject(fhandle, parent) for i in range(n)]


class RHKObject:
    """.. py:class:: RHKObject()

    Class for RHKObject, used as the parent class for the data
structure defined by RHK.

    Attributes
    --------------
    objtype: int

    offset: int

    size: int

"""

    packer = ExtStruct("<3I")
    """format is '<3I'
"""

    classes = {}

    @classmethod
    def registObjType(self, obj_id, obj_name):
        RHKObject.classes[obj_id] = obj_name
        """.. py:classmethod:: registObjType(parameters)

        Register object whose class is defined.

        Parameters
        -------------
        obj_id: int
            The object id
        obj_name: object

"""

    objectIds = [
        "Undefined",
        "PageIndexHeader",
        "PageIndexArray",  # 0 1 2
        "PageHeader",
        "PageData",
        "ImageDriftHeader",  # 3 4 5
        "ImageDrift",
        "SpecDriftHeader",
        "SpecDriftData",  # 6 7 8
        "ColorInfo",
        "StringData",
        "TipTrackHeader",  # 9 10 11
        "TipTrackData",
        "PRM",
        "Thumbnail",  # 12 13 14
        "PRMHeader",
        "ThumbnailHeader",
        "AppInfo",
    ]  # 15 16 17
    """list for object id defined by RHK"""

    def __init__(self, fhandle, parent):
        self.parent = parent
        self.objtype, self.offset, self.size = RHKObject.packer.unpack_from_file(
            fhandle
        )
        self.objname = ""
        self.children = []
        if self.objtype in RHKObject.classes:
            self.objname = RHKObject.objectIds[self.objtype]
            objclass = RHKObject.classes[self.objtype]
            if hasattr(objclass, "read"):
                self.read = MethodType(objclass.read, self)
            if hasattr(objclass, "__str__"):
                self.__str__ = MethodType(objclass.__str__, self)

    def __str__(self):
        if self.objtype in RHKObject.classes:
            return RHKObject.classes[self.objtype].__str__(self)

        this = "RHKObject of type {0.objtype} @ {0.offset} x {0.size}".format(
            self
        )
        if self.children:
            return this + "\n" + "\n".join(str(c) for c in self.children)
        else:
            return this

    def read(self, fhandle):
        """.. py:method:: read(fhandle)

        Attributes
        ----------
        fhandle: io.IOBase
            File handle
"""
        fhandle.seek(self.offset)
        self.contents = fhandle.read(self.size)

    def read_children(self, fhandle):
        """.. py:method:: read_children(fhandle)

        Attributes
        -----------
        fhandle: io.IOBase
            File handle
"""
        for child in self.children:
            #            print(self.offset, child.objtype, child.size)
            child.read(fhandle)


class RHKPageIndexHeader:  # Object Id: 1
    """.. py::class:: RHKPageIndexHeader

    Class for RHK Page Index Header

    The page index header stores the details of page index array,
which contains the array of page offsets and other info.  Using the
index array we can locate the required page data, thumbnail data for
the respective page, etc without reading th eentire SM4 file


    .. seealso::

    rhk_sm4_read_page_index_header in rhk-sm4.c

    Attributes
    ----------------
    pagecount: int
        The number of pages
    children: list
        list object that contains following child objects

        1. Page Index Array
    reserved: int
        0   (Not used, just prepared for future by RHK)
    """

    packer = ExtStruct("<4I")
    """format is '<4I'
"""

    def read(self, fhandle):
        """.. py:method:read(file)

        Reader for Page Index Header. This method should not be
        directly by the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle
"""
        fhandle.seek(self.offset)
        header = RHKPageIndexHeader.packer.unpack_from_file(fhandle)
        self.pagecount = header[0]
        self.children = get_objects_from_list(fhandle, header[1], self)
        self.reserved = header[2:]
        self.read_children(fhandle)

    def __str__(self):
        return "RHKPageIndexHeader:@{0.offset} x {0.size}\n  ".format(
            self
        ) + "\n".join(str(child) for child in self.children)


class RHKPage:
    """.. class:py::RHKPage

    Class for RHK Page

    Attributes
    ----------------
    page_id: str

    datatype: int

    datatype_name: str

    soucetype: int
        number of sourcetype
    sourcetype_name: str

    pagecount: int

    children: list

        Object List: Stores the Page Index Objects.  Currently we are
        storing:

        1. Page Header
        2. Page Data
        3. Thumbnail
        4. Thumbnail header

    reserved: int
       0  (Not used, just prepared for future by RHK)

"""

    packer = ExtStruct("<16s4I")
    """format is '<16s4I'
"""

    def __init__(self, fhandle):
        datatypes = [
            "image data",
            "line/spectra data",
            "xy_data",
            "annoted line/spectral data",
            "text_data",
            "text_annotate",
            "Sequential_data",
        ]
        sourcetypes = [
            "raw page",
            "processed page",
            "calculated page",
            "imported page",
        ]
        self.page_id, self.datatype, self.sourcetype, self.objcount, self.minorversion = RHKPage.packer.unpack_from_file(
            fhandle
        )
        self.datatype_name = datatypes[self.datatype]
        self.sourcetype_name = sourcetypes[self.sourcetype]
        self.children = get_objects_from_list(fhandle, self.objcount, self)

    def read(self, fhandle):
        """.. py:method:: read(fhandle)

        Reader for Page Index Array.  This method should not be
        directly by the user

        Attributes
        -----------
        fhandle: io.IOBase
            file handle
"""
        for child in self.children:
            child.read(fhandle)

    def __str__(self):
        return "RHKPage:\n" + "\n".join(str(child) for child in self.children)


class RHKPageIndexArray:  # Object Id: 2
    """.. py:class:: RHKPageIndexArray

    Class for RHK Page Index Array (RHK object id: 2)

    Attributes
    -----------
    pages: list
        List for storing RHKPage objects
"""

    def read(self, fhandle):
        """.. py:method:: read(file)

        Reader for Page Index Array.  This method should not be
        directly by the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle
"""

        fhandle.seek(self.offset)
        self.pages = [RHKPage(fhandle) for i in range(self.parent.pagecount)]
        for page in self.pages:
            page.read(fhandle)

    def __str__(self):
        this = "RHKPageIndexArray @ {0.offset} x {0.size}".format(self)
        that = "\n".join(str(page) for page in self.pages)
        return this + "\n" + that


class RHKPageHeader:  # Object id: 3
    """.. py::class:: RHKPageHeader

    Class for RHK Page Header. (RHK object id : 3)

    Attributes
    -----------
    fieldsize: int
        The total size of page parameters
    strcount:int
        The number of the strings in the page
    page:int
        The kind of data that an image represents.

        0. undefined
        1. topographic image
        2. curent image
        3. aux image
        4. force image
        5. signal image
        6. image FFT transform
        7. noise power spectrum
        8. line test
        9. oscilloscope
        10. image IV 4x4
        11. image IV 8x8

    datasubsource: int
        Additional information on the stored data page.
    linetype:int
        The kind of data is represented by a line or spetral page

         0. not a line
         1. histogram
         2. cross section
         3. line test
         4. oscilloscope
         5. reserved
         6. noise power spectrum
         7. I-V spectrum
         8. I-Z spectrum
         9. image X average
         10. image Y average
         11. noise autocorrelation spectrum
         12. multichannel analyzer data
         13. renormalized IV data from variable gap IV
         14. image histogram spectra
         15. image cross section
         16. image avearge
         17. image cross section (Gsection_fdata)
         18. image out spectra (Goutspec)
         19. Datalog Spectrum (Gdatalog)
         20. Gxy
         21. Electro chemistry (Gechem)
         22. Discrete Spectroscopy (Gdiscspec_data)

    x_coord, y_coord: int
        The corner position in pixel
    x_size, y_size: int
        The pixel width and the height of the image
    image_type: int

        0. raw page
        1. processed page
        2. calculated page
        3. imported page
    scan_dir: int
        The scan direction in an image.

        0. right
        1. left
        2. up
        3. down

    group_id: int
    data_size: int
        Total number of data bytes in the data section
    min_z_value, max_z_value: int
        minimum and maximum Z values
    x_scale, y_scale, z_scale: float
        The X, Y, Z physical units per **pixel** or **bit**.
    xy_scale: float
        The change in X in physical units per Y line, used for drift
        correctino.
    x_offset, y_offset, z_offset: float
        The origin of the X, value or the X coord of the image
        center.  The physical unit is 'x_offset' + 'x_scale' + (x
        number)
    period: float
        The time to acquire each data point.
    bias: float
        The sample bias in volts.
    current: float
        The absolute value of the sample current in amps.
    angle: float
        The angle by which the image is rotated.
    colorinfocount: int
        The number of color info
    grid_x_size, grid_y_size: int
        Spectral grid size in X and Y.
    objcount: int
        The count of objects after page header.


    .. seealso::

       rhk_sm4_read_page_header in rhk-sm4.c
"""

    packer = ExtStruct("<2H3I7iI2i11f3iI64B")
    """format is '<2H3I7iI2i11f3iI64B'
"""

    def read(self, fhandle):
        """.. py:method:: read(file)

        Reader for Page Header.  This method should not be directly by
        the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle

        """
        fhandle.seek(self.offset)
        self.header = RHKPageHeader.packer.unpack_from_file(fhandle)
        self.fieldsize = self.header[0]
        self.strcount = self.header[1]
        self.page = self.header[2]
        self.datasubsource = self.header[3]
        self.linetype = self.header[4]
        self.x_coord = self.header[5]
        self.y_coord = self.header[6]
        self.x_size = self.header[7]
        self.y_size = self.header[8]
        self.image_type = self.header[9]
        self.scan_dir = self.header[10]
        self.group_id = self.header[11]
        self.data_size = self.header[12]
        self.min_z_value = self.header[0]
        self.max_z_value = self.header[14]
        # float
        # scale
        self.x_scale = self.header[15]
        self.y_scale = self.header[16]
        self.z_scale = self.header[17]
        self.xy_scale = self.header[18]
        # offset
        self.x_offset = self.header[19]
        self.y_offset = self.header[20]
        self.z_offset = self.header[21]
        #
        self.period = self.header[22]
        self.bias = self.header[23]
        self.current = self.header[24]
        self.angle = self.header[25]
        # int
        self.colorinfocount = self.header[26]
        self.grid_x_size = self.header[27]
        self.grid_y_size = self.header[28]
        self.objcount = self.header[29]
        #
        self.children = get_objects_from_list(fhandle, self.objcount, self)
        self.read_children(fhandle)

    def __str__(self):
        return "RHKPageHeader @ {0.offset} x {0.size}\n  ".format(
            self
        ) + "\n  ".join(str(child) for child in self.children)


class RHKPageData:
    """ .. py::class:: RHKPageData

     Class for RHK Page data.
     the most important information (Mapping data, spectral data)

    Attributes
    -----------
    data: tuple
        The matrix data. Note that the item is int for STM/QPI image
"""

    def read(self, fhandle):
        """.. py:method:: read(file)

        Reader for Page Data.  This method should not be directly by the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle
"""
        if self.parent.datatype == 0:
            packstr = "<" + str(self.size // 4) + "l"
            RHKPageData.packer = ExtStruct(packstr)
            fhandle.seek(self.offset)
            self.data = RHKPageData.packer.unpack_from_file(fhandle)
        else:
            pass  # not implemented for spectrum

    def __str__(self):
        return "RHKPageData: @{0.offset} x {0.size}\n  ".format(self)


class RHKStringData:  # Object id: 10
    """.. py:class:: RHKStringData

    Class for RHK string. (RHK object id : 10)
"""

    packer = ExtStruct("<H")
    """format is '<H'
"""

    def read(self, fhandle):
        """.. py:method:: read(file)

        Reader for String Data.  This method should not be directly by the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle
"""
        fhandle.seek(self.offset)
        self.strings = []
        for ins in range(self.parent.strcount):
            strlen = RHKStringData.packer.unpack_from_file(fhandle)[0]
            self.strings.append(fhandle.read(strlen * 2).decode("utf-16"))

    def __str__(self):
        return "RHKStringData @ {0.offset} x {0.size}\n ".format(
            self
        ) + "\n ".join(self.strings)


class RHKPRMHeader:  # Object id: 15
    """.. py:class::RHKPRMHeader

    Class for RHK PRM Header. (RHK object id : 15)
"""

    packer = ExtStruct("<3I")
    """format is '<3I'
"""

    def read(self, fhandle):
        """.. py:method:read(file)

        Reader for PRM Header.  This method should not be directly by the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle
"""
        fhandle.seek(self.offset)
        self.header = RHKThumbnailHeader.packer.unpack_from_file(fhandle)
        self.compression = self.header[0]
        self.originalsize = self.header[1]
        self.compressionsize = self.header[2]

    def __str__(self):
        return "RHKPRMHeader @ {0.offset} x {0.size}\n ".format(self)


class RHKThumbnailHeader:  # Object id: 16
    """.. py:class::RHKThumbnailHeader

    Class for RHK Thumbnail header. (RHK object id : 16)

    Attributes
    --------------
    width: int
       Pixel width
    height: int
       Lines per frame
    nformat:int
       0 (= Raw data)
"""

    packer = ExtStruct("<3I")
    """format is '<3I'
    """

    def read(self, fhandle):
        """.. py:method:read(file)

        Reader for Thumbnail header.  This method should not be
        directly by the user

        Parameters
        ------------
        fhandle: io.IOBase
            file handle
"""
        fhandle.seek(self.offset)
        self.header = RHKThumbnailHeader.packer.unpack_from_file(fhandle)
        self.width = self.header[0]
        self.height = self.header[1]
        self.nformat = self.header[2]

    def __str__(self):
        return "RHKThumbnailHeader @ {0.offset} x {0.size}\n ".format(self)


RHKObject.registObjType(1, RHKPageIndexHeader)
RHKObject.registObjType(2, RHKPageIndexArray)
RHKObject.registObjType(3, RHKPageHeader)
RHKObject.registObjType(4, RHKPageData)
# RHKObject.registObjType(5, RHKImageDriftHeader)
# RHKObject.registObjType(6, RHKImageDrift)
# RHKObject.registObjType(7, RHKSpecDriftHeader)
# RHKObject.registObjType(8, RHKSpecDriftData)
# RHKObject.registObjType(9, RHKColorInfo)
RHKObject.registObjType(10, RHKStringData)
# RHKObject.registObjType(11, RHKTipTrackHeader)
# RHKObject.registObjType(12, RHKTipTrackData)
# RHKObject.registObjType(13, RHKPRM)
# RHKObject.registObjType(14, RHKThumbnail)
RHKObject.registObjType(15, RHKPRMHeader)
RHKObject.registObjType(16, RHKThumbnailHeader)


class SM4File:
    """.. py:class:: SM4File(file)

    Class for Loading SM4 file

    Attributes
    -------------
    signature: str

    pagecount:int
       The total pages in the file
    children:list
       The list contains the child objects.

       1. Page index Header
       2. PRM Data
       3. PRM Header

    reserved:int
        0   (Not used, just prepared for future by RHK)
    ndata: int


    Paramters
    ----------
    file: str or io.IObase
        File name or file handle of 'SM4'
    """

    packer = ExtStruct("<36s5I")
    """format is '<36s5I'
"""

    def __init__(self, filename):
        if isinstance(filename, str):
            fhandle = open(filename, "rb")
        elif isinstance(filename, io.IOBase):
            fhandle = filename
        with fhandle:
            fhandle.seek(0)
            headersize = struct.unpack("H", fhandle.read(2))[0]
            header = SM4File.packer.unpack_from_file(fhandle)
            if headersize > SM4File.packer.size:
                self.header_pad = fhandle.read(
                    headersize - SM4File.packer.size
                )
            self.signature = header[0]
            self.pagecount = header[1]
            self.children = get_objects_from_list(fhandle, header[2], self)
            self.reserved = header[4:]
            for child in self.children:
                child.read(fhandle)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    SM4 = SM4File(filename)
    for child in SM4.children:
        print(child)
