from iarlib.reader import Reader
from iarlib.symbol import Symbol
from iarlib.segment import Segment
from iarlib.opcode import OpCode


class Abs8:
    ID = 0x36
    def __repr__(self):
        return f'{self.value!r}'
    def __init__(self, data: Reader):
        self.value = OpCode(data)

class Abs16:
    ID = 0x37
    def __init__(self, data: Reader):
        self.value = data.readU16()

class Pop8:
    ID = 0x5A
    def __init__(self, data: Reader):
        pass

class PushExt: # External symbol?
    ID = 0x5D
    def __repr__(self):
        return f'PUSHEXT {self.symbol!r}'
    def __init__(self, data: Reader):
        self.symbol = Symbol.getExternal(data.readDynamic())
        data.readU32() # Unknown

class PushRel:
    ID = 0x5E
    def __repr__(self):
        return f'PUSHREL {self.symbol!r}'
    def __init__(self, data: Reader):
        self.symbol = Symbol.getRelocatable(data.readDynamic())
        data.readU32() # Unknown

class PushAbs:
    ID = 0x61
    def __init__(self, data: Reader):
        self.value = data.readU32()

class PushPcr:
    ID = 0x62
    def __init__(self, data: Reader):
        self.value = data.readU32() # Unknown

class Minus:
    ID = 0x64
    def __init__(self, data: Reader):
        pass # These decrement the stack when shared pops are used (sjmp)

class DeleteTos: # Purpose?
    ID = 0x9C
    def __init__(self, data: Reader):
        pass

class Pop24:
    ID = 0xA4
    def __init__(self, data: Reader):
        pass

class OrgRel:
    ID = 0xC7
    def __repr__(self):
        if isinstance(self.value, Symbol):
            return f'{self.value!r}'
        else:
            return f'.area {self.value!r}\n.org 0x{self.offset:08X}'
    def __init__(self, data: Reader):
        idx = data.readDynamic()
        self.value = Symbol.getRelocatable(idx)
        if self.value is None:
            self.value = Segment.get(idx)
        self.offset = data.readU32() # Unknown
        print(self)

assembly_modes = {
    0x01: "CODE",
    0x0A: "DATA",
}
class AssemblyMode:
    ID = 0xDE
    def __init__(self, data: Reader):
        self.mode = data.readU8()