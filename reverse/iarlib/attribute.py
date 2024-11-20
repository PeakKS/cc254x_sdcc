from iarlib.reader import Reader

types = {
    1: "function",
}

class Attribute:
    def ID():
        return 0xD3
    def __init__(self, data: Reader):
        data.readU16() # Size
        self.type = types.get(data.readU8())
        data.readU8() # Index
        self.name = data.readString()
