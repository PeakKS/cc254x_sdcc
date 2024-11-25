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
    ID = 0xC4
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

function_table = {}

def getFunction(index):
    return function_table.get(index)

class Function:
    def __str__(self):
        ret = f'FUNC={self.func_index:04X} FILE={self.file:04X} LINE={self.line:04X} DEF={self.func_def:08X}\n'
        for count in self.counts:
            ret += f'\t{count}\n'
        return ret[:-1]
    
    def __repr__(self):
        return f'{self.symbol!r}'
    
    def __init__(self, symbol, data: Reader):
        self.symbol = symbol
        self.func_index = data.readU16()
        self.file = data.readU16()
        self.line = data.readU16()
        self.func_def = data.readU32()
        data.readU16() # Unknown
        self.counts = []
        while(data.peekU8(0) == FrameCount.ID):
            data.readU8()
            self.counts.append(FrameCount(data))
        function_table[self.func_index] = self

class ExternalFunction:
    def __str__(self):
        ret = f'XFUNC={self.func_index:04X} DEF={self.func_def:08X}\n'
        for count in self.counts:
            ret += f'\t{count}\n'
        return ret[:-1]
    
    def __repr__(self):
        return f'{self.symbol!r}'

    def __init__(self, symbol, data: Reader):
        self.symbol = symbol
        self.func_index = data.readU16()
        self.func_def = data.readU32()
        self.counts = []
        while(data.peekU8(0) == 0xC4):
            data.readU8()
            self.counts.append(FrameCount(data))
        function_table[self.func_index] = self

sub_def_map = {
    0xB0: Function,
    0xB1: ExternalFunction,
}

location_names = {
    0x02: "PUBLIC_REL",
    0x05: "EXTERNAL",
}

relocatable_table = {}
external_table = {}

location_map = {
    0x02: relocatable_table,
    0x05: external_table,
}

class Symbol:
    ID = 0xCE
    
    def __str__(self):
        ret = f'{location_names[self.location]} {self.type} {self.name}\n{self.func}'
        return ret[:-1]
    
    def __repr__(self):
            if self.func is not None:
                return f'{self.name} {self.type!r}'
            else:
                return f'{self.type!r} {self.name}'

    def __init__(self, data: Reader):
        global relocatable_table
        global external_table
        data.readU32() # Unknown
        self.location = data.readU8()
        self.index = data.readDynamic()
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
        if sub_def_map.get(data.peekU8(0)) is not None:
            self.func = sub_def_map.get(data.readU8())(self, data)
        else:
            self.func = None
        location_map[self.location][self.index] = self

    def getRelocatable(index):
        return relocatable_table.get(index)
    
    def getExternal(index):
        return external_table.get(index)

class SourceCall:
    ID = 0xCB
    def __repr__(self):
        return f'Call Flags: {self.flags:04X}'
    def __init__(self, data: Reader):
        self.caller = getFunction(data.readU16())
        self.callee = getFunction(data.readU16())
        self.flags = data.readU16()
        self.counts = []
        while(data.peekU8(0) == FrameCount.ID):
            data.readU8()
            self.counts.append(FrameCount(data))
        print(f';Call to external function {self.callee!r} with flags {self.flags:04X}')