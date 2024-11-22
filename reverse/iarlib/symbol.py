from iarlib.reader import Reader
from iarlib.nametable import NameTable
from iarlib.type import Type

class FrameSize:
    def __repr__(self):
        return f'SNO={self.SNO:02X} {self.size:08X} {self.flags:04X}'
    
    def __init__(self, data: Reader):
        self.SNO = data.readU8()
        self.size = data.readU32()
        self.flags = data.readU16()

class FrameCount:
    def __str__(self):
        ret = f'Frames:\n'
        for fs in self.frame_sizes:
            ret += f'\t{fs}\n'
        return ret[:-1]
    
    def __init__(self, data: Reader):
        count = data.readU32()
        self.frame_sizes = []
        for _ in range(count):
            data.readU8()
            self.frame_sizes.append(FrameSize(data))

class Function:
    def __str__(self):
        ret = f'FUNC={self.func_index:04X} FILE={self.file:04X} LINE={self.line:04X} DEF={self.func_def:08X}\n'
        for count in self.counts:
            ret += f'\t{count}\n'
        return ret[:-1]
    
    def __init__(self, data: Reader):
        self.func_index = data.readU16()
        self.file = data.readU16()
        self.line = data.readU16()
        self.func_def = data.readU32()
        data.readU16() # Unknown
        self.counts = []
        while(data.peekU8(0) == 0xC4):
            data.readU8()
            self.counts.append(FrameCount(data))

class ExternalFunction:
    def __str__(self):
        ret = f'XFUNC={self.func_index:04X} DEF={self.func_def:08X}\n'
        for count in self.counts:
            ret += f'\t{count}\n'
        return ret[:-1]

    def __init__(self, data: Reader):
        self.func_index = data.readU16()
        self.func_def = data.readU32()
        self.counts = []
        while(data.peekU8(0) == 0xC4):
            data.readU8()
            self.counts.append(FrameCount(data))

sub_def_map = {
    0xB0: Function,
    0xB1: ExternalFunction,
}

class Symbol:
    ID = 0xCE
    
    def __repr__(self):
        ret = f'SYMBOL {self.type} {self.name}\n'
        for sub in self.sub_defs:
            ret += f'\t{sub}\n'
        return ret[:-1]

    def __init__(self, data: Reader):
        data.readU32() # Unknown
        data.readU8() # Unknown
        self.index = data.readU8()
        data.readU8() # Unknown
        data.readU8() # Unknown
        data.readU8() # Unknown
        data.readU8() # Unknown
        data.readU8() # Unknown
        data.readU8() # Unknown
        data.readU8() # Unknown
        self.name = NameTable.get(data.readU8())
        self.type = Type.get(data)
        data.readU8()
        data.readU8()
        data.readU8()
        self.sub_defs = []
        if sub_def_map.get(data.peekU8(0)) is not None:
            self.sub_defs.append(sub_def_map.get(data.readU8())(data))