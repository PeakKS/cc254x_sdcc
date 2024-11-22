from iarlib.reader import Reader

size_map = {
    # Intrinsic types
    0x01: "unsigned char",
    0x02: "signed char",
    0x03: "unsigned short",
    0x04: "signed short",
    0x05: "unsigned int",
    0x06: "signed int",
    0x07: "unsigned long",
    0x08: "signed long",
    0x09: "float",
    0x0A: "double",
    0x0B: "long double",
    0x2D: "unsigned long long",
    0x2E: "signed long long",
    0x2F: "bool",
    0x30: "wchar_t",
    0x36: "unsigned char", # Why?
}

class SizeType:
    ID = 0x4F
    def __repr__(self):
        return f'{size_map[self.type]} = {self.size}'
    def __init__(self, data: Reader):
        self.type = data.readU8()
        self.size = data.readU8()