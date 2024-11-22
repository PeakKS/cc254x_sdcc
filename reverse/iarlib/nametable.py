from iarlib.reader import Reader

names = []

class NameTable:
    ID = 0xCD
    def __repr__(self):
        return self.name
    def __init__(self, data: Reader):
        global names
        data.readU32() # Size
        data.readU32() # Unknown
        self.name = data.readString()

        refIndex = data.readU32()
        if refIndex != 0xFFFFFFFF:
            self.name = names[refIndex] + self.name

        names.append(self.name)
    def get(index: int):
        if (index == 0xFFFFFFFF):
            return None
        return names[index]