from iarlib.reader import Reader

class StackError:
    ID = 0x9D
    def __init__(self, data: Reader):
        self.error = data.readString()

class Check:
    ID = 0x73
    def __init__(self, data: Reader):
        self.upper = data.readU32()
        self.lower = data.readU32()

class Copy:
    ID = 0x70
    def __init__(self, data: Reader):
        pass

class LSR:
    ID = 0x6E
    def __init__(self, data: Reader):
        data.readU32() # Unknown