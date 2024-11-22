from iarlib.reader import Reader

types = {
    0x06: "__xdata",
    0x15: "__banked_func",
}

class PointerType:
    ID = 0xC1
    def __init__(self, data: Reader):
        self.static = types.get(data.readU8())
        self.auto = types.get(data.readU8())
        self.const = types.get(data.readU8())
        self.general = types.get(data.readU8())
        self.code = types.get(data.readU8())