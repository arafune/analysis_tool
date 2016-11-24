# -*- coding: utf-8 -*-
'''.. py:module:: rhksm4

Module to read the proprietary files SM4 from RHK technology

For writing the code I used some ideas from the Gwyddion project
(http://gwyddion.net/) where I found rhk-sm4.c. Some of variable names
are followed from it.
'''

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


    def __init__(self, fhandle, parent):
        self.parent = parent
        self.objtype, self.offset, self.size = \
                        RHKObject.packer.unpack_from_file(fhandle)
        self.children = []
        if self.objtype in RHKObject.classes:
            objclass = RHKObject.classes[self.objtype]
            if hasattr(objclass, 'read'):
                self.read = MethodType(objclass.read, self)
            if hasattr(objclass, '__str__'):
                self.__str__ = MethodType(objclass.__str__, self)

    def read(self, fhandle):
        fhandle.seek(self.offset)
        self.contents = fhandle.read(self.size)
            
            
        
class RHKPageIndexHeader:
    pass


class RHKPageIndexArray:
    pass


class RHKPageHeader:
    pass


class RHKStringData:
    pass


RHKObject.registObjType(1, RHKPageIndexHeader)
RHKObject.registObjType(2, RHKPageIndexArray)
RHKObject.registObjType(3, RHKPageHeader)
#RHKObject.registObjType(4, RHKPageData)
#RHKObject.registObjType(5, RHKImageDriftHeader)
#RHKObject.registObjType(6, RHKImageDrift)
#RHKObject.registObjType(7, RHKSpecDriftHeader)
#RHKObject.registObjType(8, RHKSpecDriftData)
#RHKObject.registObjType(9, RHKColorInfo)
RHKObject.registObjType(10, RHKStringData)
#RHKObject.registObjType(11, RHKTipTrackHeader)
#RHKObject.registObjType(12, RHKTipTrackData)
#RHKObject.registObjType(13, RHKPRM)
#RHKObject.registObjType(14, RHKThumbnail)
#RHKObject.registObjType(15, RHKPRMHeader)
#RHKObject.registObjType(16, RHKThumbnailHeader)


class SM4File:
    '''Loader for SM4 file'''

    packer = ExtStruct('<36s5I')

    def __init__(self, filename):
        with open(filename, 'rb') as f:
            f.seek(0)
            headersize = struct.unpack('H', f.read(2))[0]
            header = SM4File.packer.unpack_from_file(f)
            if headersize > SM4File.packer.size:
                self.header_pad = f.read(headersize - SM4File.packer.size)
            self.signature = header[0]
            self.pagecount = header[1]
            self.children = get_objects_from_list(f, header[2], self)
            self.reserved = header[4:]
            for child in self.children:
                child.read(f)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    SM4 = SM4File(filename)
    for child in SM4.children:
        print(child)
