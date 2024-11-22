from datetime import date
from iarlib.reader import Reader

class Library:
    ID = 0x00
    def __str__(self):
        return f'{self.name}.c {self.date} REV={self.revision} CPA={self.cpa}'
    def __repr__(self):
        return self.name
    def __init__(self, data: Reader):
        self.revision = data.readU8()
        self.cpa = data.readU8()
        year = data.readU8()
        month = data.readU8()
        day = data.readU8()
        self.date = date(2000 + year, month, day)
        data.readU8() # Unknown (LAN?)
        self.name = data.readString()

class Version:
    ID = 0xBD
    def __repr__(self):
        return f'{self.major}.{self.minor}.{self.revision}'
    def __init__(self, data: Reader):
        self.major = data.readU8()
        self.minor = data.readU8()
        self.revision = data.readU8()
        data.readU8() # Unknown (padding?)

class Auxillary:
    ID = 0x53
    def __init__(self, data: Reader):
        self.flags = data.readU16()

class Auxillary1:
    ID = 0x54
    def __init__(self, data: Reader):
        self.flags = data.readU16()
        self.version = data.readString()

class End:
    ID = 0x3F
    def __init__(self, data:Reader):
        self.crc = data.readU16()