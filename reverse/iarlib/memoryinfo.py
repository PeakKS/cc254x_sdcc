from iarlib.reader import Reader

intrinsic_map = {
    # Intrinsic types
    0x01: "unsigned char",
    0x02: "signed char",
    0x03: "unsigned short",
    0x04: "signed short",
    0x05: "unsigned int",
    0x06: "signed int",
    0x07: "unsigned long",
    0x08: "signed long",
}

meminfo_map = {}

class MemoryInfo:
    def ID():
        return 0xC6
    def __repr__(self):
        return self.name
    def __init__(self, data: Reader):
        global meminfo_map
        data.readU16() # Size
        self.index = data.readU8()
        self.pointer_size = data.readU8()
        self.type = intrinsic_map.get(data.readU8())
        self.flags = data.readU8()
        length = data.readU32()
        self.name = data.readStringLength(length)
        meminfo_map[self.index] = self
    def get(index: int):
        return meminfo_map.get(index)