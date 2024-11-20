from iarlib.reader import Reader
from iarlib.nametable import NameTable
from iarlib.memoryinfo import MemoryInfo

type_map = {
    # Intrinsic types
    0x00: "void",
    0x01: "unsigned char",
    0x02: "signed char",
    0x03: "unsigned short",
    0x04: "signed short",
    0x05: "unsigned int",
    0x06: "signed int",
    0x07: "unsigned long",
    0x08: "signed long",
}

def readIndex(data: Reader):
    index = data.readU8()
    if index >= 0x80:
        data.readU8() # 0x01 appended for values above 0x80 (why?)
    return index

class Pointer:
    def __repr__(self):
        return f'({self.target} *)'
    def __init__(self, data: Reader):
        self.target = Type.get(data)

class Function:
    def __repr__(self):
        repr = f'{self.return_type} ('
        for p in range(len(self.params)):
            repr += f'{self.params[p]} ARG{p}, '
        repr = repr.removesuffix(', ') + '){\n}'
        return repr
    def __init__(self, data: Reader):
        self.return_type = Type.get(data)
        self.format = data.readU8()
        param_count = data.readU8()
        self.params = []
        for _ in range(param_count):
            self.params.append(Type.get(data))

class Array:
    def __repr__(self):
        return f'{self.type} [{self.count}]'
    def __init__(self, data: Reader):
        self.type = Type.get(data)
        self.size = data.readU32()
        self.count = data.readU32()

class DataAttribute:
    def __str__(self):
        return str(self.memory_info)
    def __repr__(self):
        return f'DATA_ATTR {self.memory_info} {self.data_type} GEN: {self.gen:08X} TGT: {self.target:08X}'
    def __init__(self, data: Reader):
        self.memory_info = MemoryInfo.get(data.readU8())
        self.data_type = Type.get(data)
        self.gen = data.readU32()
        data.readU8() # Unknown
        self.target = data.readU32()

class FunctionAttribute:
    def __str__(self):
        return str(self.memory_info)
    def __repr__(self):
        return f'FUNC_ATTR {self.memory_info} {self.func_type} GEN: {self.gen:08X} TGT: {self.target:08X}'
    def __init__(self, data: Reader):
        self.memory_info = MemoryInfo.get(data.readU8())
        self.func_type = Type.get(data)
        self.gen = data.readU32()
        data.readU8() # Unknown
        self.target = data.readU32()

class Typedef:
    def __str__(self):
        return self.name
    def __repr__(self):
        return f'typedef {self.reference_type} {self.name}'
    def __init__(self, data: Reader):
        self.reference_type = Type.get(data)
        self.name = NameTable.get(data.readU32())

class StructUnionMember:
    def __repr__(self):
        return f'\t{self.type} {self.name}\n'
    def __init__(self, data: Reader):
        data.readU32() # Index
        self.name = NameTable.get(data.readU32())
        self.type = Type.get(data)
        data.readU32() # Unknown

class StructUnion:
    def __repr__(self):
        repr = ''
        if self.type == 9:
            repr += 'struct {\n'
        else:
            repr += 'union {\n'
        for member in self.members:
            repr += f'{member}'
        repr += '}'
        return repr
    def __init__(self, data: Reader):
        self.name = NameTable.get(data.readU32())
        self.type = data.readU32() # Struct or union
        self.size = data.readU32()
        member_count = data.readU32()
        self.members = []
        for _ in range(member_count):
            self.members.append(StructUnionMember(data))

subtype_map = {
    0x0F: Pointer,
    0x14: Function,
    0x29: Array,
    0x2A: DataAttribute,
    0x2B: FunctionAttribute,
    0x31: Typedef,
    0x34: StructUnion,
}

class Type:
    def ID():
        return 0x4A
    def __repr__(self):
        return repr(type_map.get(self.index))
    def __init__(self, data: Reader):
        global type_map
        self.index = readIndex(data)
        subtype = data.readU8()
        type_map[self.index] = subtype_map.get(subtype)(data)
        
    def get(data: Reader):
        return type_map.get(readIndex(data))