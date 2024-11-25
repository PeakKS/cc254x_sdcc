from iarlib.reader import Reader

type_map = {
    0x21: "CODE",
    0x22: "DATA",
    0x23: "XDATA",
    0x24: "IDATA",
    0x27: "CONST",
}

spa_map = {
    0x00: "NORMAL",
    0x20: "REORDER",
}

segment_map = {}

class Segment:
    ID = 0x4B
    def __str__(self):
        return f'{self.index:02X}: {self.name} {self.type} SPA={self.SPA}'
    def __repr__(self):
        return f'{self.name} (REL,{self.type})'
    def __init__(self, data: Reader):
        self.SPA = spa_map[data.readU8() - 0x80] # Why?
        self.index = data.readU8()
        self.type = type_map[data.readU8()]
        self.name = data.readString()
        segment_map[self.index] = self
    def get(index):
        return segment_map.get(index)