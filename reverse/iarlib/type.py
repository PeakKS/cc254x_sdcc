from iarlib.reader import Reader
from iarlib.nametable import NameTable
from iarlib.memoryinfo import MemoryInfo

class Intrinsic:
    def __repr__(self):
        return self.name
    def __init__(self, name, size):
        self.name = name
        self.size = size

type_map = {
    # Intrinsic types
    0x01: Intrinsic("unsigned char", 1),
    0x02: Intrinsic("signed char", 1),
    0x03: Intrinsic("unsigned short", 2),
    0x04: Intrinsic("signed short", 2),
    0x05: Intrinsic("unsigned int", 4),
    0x06: Intrinsic("signed int", 4),
    0x07: Intrinsic("unsigned long", 4),
    0x08: Intrinsic("signed long", 4),
    0x09: Intrinsic("float", 4),
    0x0A: Intrinsic("double", 4),
    0x0B: Intrinsic("long double", 4),
    0x0C: Intrinsic("void", 0),
    0x2D: Intrinsic("unsigned long long", 4),
    0x2E: Intrinsic("signed long long", 4),
    0x2F: Intrinsic("bool", 1),
    0x30: Intrinsic("wchar_t", 2),
    0x36: Intrinsic("char (unsigned)", 1), # Why??
}

class Pointer:
    def __repr__(self):
        return f'({self.target!r} *)'
    def __init__(self, data: Reader):
        self.target = Type.get(data)

class Function:
    def __repr__(self):
        return f'{self.return_type!r}' + self.args()
    def __init__(self, data: Reader):
        self.return_type = Type.get(data)
        self.format = data.readU8()
        param_count = data.readU8()
        self.params = []
        for _ in range(param_count):
            self.params.append(Type.get(data))
    def args(self):
        ret = '('
        for p in range(len(self.params)):
            ret += f'{self.params[p]!r}, '
        return ret.removesuffix(', ') + ')'

class Array:
    def __repr__(self):
        return f'{self.type!r} [{self.count}]'
    def __init__(self, data: Reader):
        self.type = Type.get(data)
        self.size = data.readU32()
        self.count = data.readU32()

class DataAttribute:
    def __repr__(self):
        if self.memory_info is None:
            return f'{self.data_type!r}'
        return f'{self.data_type!r} {self.memory_info}'
    def __init__(self, data: Reader):
        mem_idx = data.readU8()
        self.memory_info = MemoryInfo.get(mem_idx)
        self.data_type = Type.get(data)
        self.gen = data.readU32()
        data.readU8() # Unknown
        self.target = data.readU32()

class FunctionAttribute:
    def __str__(self):
            return f'{self.func_type!r} {self.memory_info}'
    def __repr__(self):
            return f'{self.func_type!r}'
    def __init__(self, data: Reader):
        mem_idx = data.readU8()
        self.memory_info = MemoryInfo.get(mem_idx)
        if self.memory_info is None:
            print(f'Memory Info {mem_idx:04X} is None!')
        self.func_type = Type.get(data)
        self.gen = data.readU32()
        data.readU8() # Unknown
        self.target = data.readU32()

class Typedef:
    def __str__(self):
        if isinstance(self.reference_type, Pointer):
            if isinstance(self.reference_type.target, FunctionAttribute):
                func = self.reference_type.target.func_type
                return f'typedef {func.return_type!r} (*{self.name})' + func.args()

        return f'typedef {self.reference_type!r} {self.name}'
    def __repr__(self):
        return self.name
    def __init__(self, data: Reader):
        self.reference_type = Type.get(data)
        self.name = NameTable.get(data.readU32())
        print(self)

class StructUnionMember:
    def __repr__(self):
        return f'\t{self.type!r} {self.name}\n'
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
    ID = 0x4A
    def __repr__(self):
        return f'{type_map.get(self.index)!r}'
    def __init__(self, data: Reader):
        global type_map
        self.index = data.readDynamic()
        subtype = data.readU8()
        type_map[self.index] = subtype_map.get(subtype)(data)
        
    def get(data: Reader):
        idx = data.readDynamic()
        type = type_map.get(idx)
        return type