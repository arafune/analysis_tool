# -*- coding: utf-8 -*-
'''.. py:module:: rhksm4

Module to read the proprietary files SM4 from RHK technology

For writing the code I used some ideas from the Gwyddion project
(http://gwyddion.net/) where I found rhk-sm4.c. Some of variable names
are followed from it.
'''

import io
import struct
from types import MethodType


class ExtStruct(struct.Struct):
    '''Helper class to treat pack/unpack smoothly'''

    def __init__(self, fmt):
        super().__init__(fmt)

    def unpack_from_file(self, fhandle):
        '''Helper function to unpack from file'''
        return self.unpack(fhandle.read(self.size))


def get_objects_from_list(fhandle, n, parent):
    return [RHKObject(fhandle, parent) for i in range(n)]


class RHKObject:

    packer = ExtStruct('<3I')

    classes = {}

    @classmethod
    def registObjType(self, obj_id, obj_name):
        RHKObject.classes[obj_id] = obj_name

    objectIds = ['Undefined', 'PageIndexHeader', 'PageIndexArray',  # 0 1 2
                 'PageHeader', 'PageData', 'ImageDriftHeader',      # 3 4 5
                 'ImageDrift', 'SpecDriftHeader', 'SpecDriftData',  # 6 7 8
                 'ColorInfo', 'StringData', 'TipTrackHeader',       # 9 10 11
                 'TipTrackData', 'PRM', 'Thumbnail',                # 12 13 14
                 'PRMHeader', 'ThumbnailHeader', 'AppInfo']         # 15 16 17

    def __init__(self, fhandle, parent):
        self.parent = parent
        self.objtype, self.offset, self.size = \
            RHKObject.packer.unpack_from_file(fhandle)
        self.objname = ""
        self.children = []
        if self.objtype in RHKObject.classes:
            self.objname = RHKObject.objectIds[self.objtype]
            objclass = RHKObject.classes[self.objtype]
            if hasattr(objclass, 'read'):
                self.read = MethodType(objclass.read, self)
            if hasattr(objclass, '__str__'):
                self.__str__ = MethodType(objclass.__str__, self)
#

    def __str__(self):
        if self.objtype in RHKObject.classes:
            return RHKObject.classes[self.objtype].__str__(self)

        this = 'RHKObject of type {0.objtype} @ {0.offset} x {0.size}'.\
               format(self)
        if self.children:
            return this + "\n" + "\n".join(str(c) for c in self.children)
        else:
            return this

    def read(self, fhandle):
        fhandle.seek(self.offset)
        self.contents = fhandle.read(self.size)

    def read_children(self, fhandle):
        for child in self.children:
            #            print(self.offset, child.objtype, child.size)
            child.read(fhandle)


class RHKPageIndexHeader:  # Object Id: 1
    '''.. py::class:: RHKPageIndexHeader

    Class for RHK Page Index Header

    The page index header stores the details of page index array,
which contains the array of page offsets and other info.  Using the
index array we can locate the required page data, thumbnail data for
the respective page, etc without reading th eentire SM4 file

    See rhk_sm4_read_page_index_header in rhk-sm4.c

    Attributes
    ----------------
    pagecount, children, reserved
    '''
    packer = ExtStruct('<4I')

    def read(self, fhandle):
        fhandle.seek(self.offset)
        header = RHKPageIndexHeader.packer.unpack_from_file(fhandle)
        self.pagecount = header[0]
        self.children = get_objects_from_list(fhandle, header[1], self)
        self.reserved = header[2:]
        self.read_children(fhandle)

    def __str__(self):
        return 'RHKPageIndexHeader:@{0.offset} x {0.size}\n  '.format(self) + \
            "\n".join(str(child) for child in self.children)


class RHKPage:
    '''.. py::class::RHKPage

    Class for RHK Page

    Attributes
    ----------------
         page_id, datatype, datatype_name,
         soucetype, sourcetype_name, pagecount, children, reserved


      Object List: Stores the Page Index Objects.  Currently we are storing:
        1. Page Header
        2. Page Data
        3. Thumbnail
        4. Thumbnail header
    '''

    packer = ExtStruct('<16s4I')

    def __init__(self, fhandle):
        datatypes = ['image data', 'line/spectra data', 'xy_data',
                     'annoted line/spectral data', 'text_data',
                     'text_annotate', 'Sequential_data']
        sourcetypes = ['raw page', 'processed page',
                       'calculated page', 'imported page']
        self.page_id, self.datatype, self.sourcetype, \
            self.objcount, self.minorversion \
            = RHKPage.packer.unpack_from_file(fhandle)
        self.datatype_name = datatypes[self.datatype]
        self.sourcetype_name = sourcetypes[self.sourcetype]
        self.children = get_objects_from_list(fhandle, self.objcount, self)

    def read(self, fhandle):
        for child in self.children:
            child.read(fhandle)

    def __str__(self):
        return "RHKPage:\n"+"\n".join(str(child) for child in self.children)


class RHKPageIndexArray:  # Object Id: 2
    '''.. py::class:: RHKPageIndexArray

    Class for RHK Page Index Array
    '''

    def read(self, fhandle):
        fhandle.seek(self.offset)
        self.pages = [RHKPage(fhandle) for i in range(self.parent.pagecount)]
        for page in self.pages:
            page.read(fhandle)

    def __str__(self):
        this = 'RHKPageIndexArray @ {0.offset} x {0.size}'.format(self)
        that = '\n'.join(str(page) for page in self.pages)
        return this + "\n" + that


class RHKPageHeader:  # Object id: 3
    '''.. py::class:: RHKPageHeader

    Class for RHK Page Header

    See rhk_sm4_read_page_header in rhk-sm4.c
    '''
    packer = ExtStruct('<2H3I7iI2i11f3iI64B')

    def read(self, fhandle):
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
        return 'RHKPageHeader @ {0.offset} x {0.size}\n  '.format(self) + \
            '\n  '.join(str(child) for child in self.children)


class RHKPageData:
    ''' .. py::class:: RHKPageData

     Class for RHK Page data.
     the most important information (Mapping data, spectral data)
     '''

    def read(self, fhandle):
        if self.parent.datatype == 0:
            packstr = "<" + str(self.size // 4) + "l"
            RHKPageData.packer = ExtStruct(packstr)
            fhandle.seek(self.offset)
            self.data = RHKPageData.packer.unpack_from_file(fhandle)
        else:
            pass  # not implemented for spectrum

    def __str__(self):
        return 'RHKPageData: @{0.offset} x {0.size}\n  '.format(self)


class RHKStringData:    # Object id: 10
    packer = ExtStruct('<H')

    def read(self, fhandle):
        fhandle.seek(self.offset)
        self.strings = []
        for ins in range(self.parent.strcount):
            strlen = RHKStringData.packer.unpack_from_file(fhandle)[0]
            self.strings.append(fhandle.read(strlen*2).decode("utf-16"))

    def __str__(self):
        return "RHKStringData @ {0.offset} x {0.size}\n ".format(self) +\
            "\n ".join(self.strings)


class RHKPRMHeader:  # Object id: 15

    packer = ExtStruct('<3I')

    def read(self, fhandle):
        fhandle.seek(self.offset)
        self.header = RHKThumbnailHeader.packer.unpack_from_file(fhandle)
        self.compression = self.header[0]
        self.originalsize = self.header[1]
        self.compressionsize = self.header[2]

    def __str__(self):
        return 'RHKPRMHeader @ {0.offset} x {0.size}\n '.format(self)


class RHKThumbnailHeader:  # Object id: 16

    packer = ExtStruct('<3I')

    def read(self, fhandle):
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
    '''Loader for SM4 file'''

    packer = ExtStruct('<36s5I')

    def __init__(self, filename):
        if isinstance(filename, str):
            fhandle = open(filename, 'rb')
        elif isinstance(filename, io.IOBase):
            fhandle = filename
        with fhandle:
            fhandle.seek(0)
            headersize = struct.unpack('H', fhandle.read(2))[0]
            header = SM4File.packer.unpack_from_file(fhandle)
            if headersize > SM4File.packer.size:
                self.header_pad = fhandle.read(headersize -
                                               SM4File.packer.size)
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
