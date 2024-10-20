import struct

 
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
 
def u32(file):
    return struct.unpack("<I", file.read(4))[0]


class FileBlock(object):
    def __init__(self,sig="NULL",blks = 8):
        self.signature = sig
        self.block_size = blks
    def read(self,f):
        self.signature = u32(f)
        self.block_size = u32(f)

class GARC(object):

    class FileAllocationOffsetBlock(object):
        def __init__(self):
            self.header = FileBlock("OTAF")
            self.file_id_num = 0
            self.offsets = []
        def read(self,f):
            self.header.read(f)
            self.file_id_num = u16(f)
            f.seek(2,1)
            for x in range(self.file_id_num):
                self.offsets.append(u32(f))
    class FileAllocationTableBlock(object):
        class TableBlock(object):
            def __init__(self):
                self.language_bit = 0
                self.file_top = 0
                self.file_bot = 0
            def fsize(self):
                return self.file_bot - self.file_top
            def offset(self):
                return self.file_top
            def read(self,f):
                self.language_bit = u32(f)
                self.file_top = u32(f)
                self.file_bot = u32(f)
        def __init__(self):
            self.header = FileBlock("BTAF")
            self.file_id_num = 0
            self.blocks = []
        def read(self,f):
            self.header.read(f)
            self.file_id_num = u32(f)
            for x in range(self.file_id_num):
                blk = self.TableBlock()
                blk.read(f)
                self.blocks.append(blk)
    class FileImageBlock(object):
        def __init__(self):
            self.header = FileBlock("BMIF",0xC)
            self.image_size = 0
        def read(self,f):
            self.header.read(f)
            self.byte_order = u32(f)
    def __init__(self):
        self.header = FileBlock("CRAG",0x18)
        self.byte_order = 0xFEFF
        self.version = 0x204
        self.block_num = 4
        self.total_block_size = 0
        self.file_size = 0
        self.faob = self.FileAllocationOffsetBlock()
        self.fatb = self.FileAllocationTableBlock()
        self.fimb = self.FileImageBlock()
        self.daFilez = []
    def read(self,f):
        self.header.read(f)
        self.byte_order = u16(f)
        self.version = u16(f)
        self.block_num = u16(f)
        f.seek(2,1)
        self.total_block_size = u32(f)
        self.file_size = u32(f)
        self.faob.read(f)
        self.fatb.read(f)
        self.fimb.read(f)
        endob = f.tell()
        for x in self.fatb.blocks:
            f.seek(endob + x.offset())
            self.daFilez.append(f.read(x.fsize()))

import sys,os

def makemydir(whatever):
    try:
        os.makedirs(whatever)
    except OSError:
        pass
    # let exception propagate if we just can't
    # cd into the specified directory
    os.chdir(whatever)

garcy = open(sys.argv[1], "rb")

garc = GARC()
garc.read(garcy)
print(hex(garc.version))

folderOut = sys.argv[1][:sys.argv[1].find('.')]

makemydir(folderOut)

for idx,x in enumerate(garc.fatb.blocks):
    #print("File Sizes: %s" % hex(x.fsize()))
    fo = open(folderOut+'\\'+str("%04i"%idx)+'.bin','wb')
    fo.write(garc.daFilez[idx])