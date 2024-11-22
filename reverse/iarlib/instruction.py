from iarlib.reader import Reader

class Abs8:
    ID = 0x36
    def __init__(self, data: Reader):
        self.value = data.readU8()

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
    def __init__(self, data: Reader):
        data.readU8() # Unknown
        data.readU32() # Unknown

class PushRel:
    ID = 0x5E
    def __init__(self, data: Reader):
        data.readU8() # Unknown
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
        pass

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
    def __init__(self, data: Reader):
        data.readU8() # Unknown
        data.readU32() # Unknown

class AssemblyMode:
    ID = 0xDE
    def __init__(self, data: Reader):
        self.mode = data.readU8()