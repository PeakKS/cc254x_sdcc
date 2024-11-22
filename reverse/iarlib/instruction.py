from iarlib.reader import Reader

class OrgRel:
    ID = 0xC7
    def __init__(self, data: Reader):
        data.readU8() # Unknown
        data.readU32() # Unknown

class AssemblyMode:
    ID = 0xDE
    def __init__(self, data: Reader):
        self.mode = data.readU8()

class PushExt: # External symbol?
    ID = 0x5D
    def __init__(self, data: Reader):
        data.readU8() # Unknown
        data.readU32() # Unknown

class DeleteTos: # Purpose?
    ID = 0x9C
    def __init__(self, data: Reader):
        pass