import os
from io import BytesIO
from typing import Tuple

class BytesReader:
    def __init__(self, bytes: bytes):
        self.bytes = bytes

    def valid(self):
        return len(self.bytes) > 0

    def parseU8(self) -> int:
        ret = int.from_bytes(self.bytes[:1])
        self.bytes = self.bytes[1:]
        return ret
    
    def peekU8(self, offset) -> int:
        return int.from_bytes(self.bytes[:1])
    
    def parseU16(self) -> int:
        ret = int.from_bytes(self.bytes[:2])
        self.bytes = self.bytes[2:]
        return ret
    
    def parseU32(self) -> int:
        ret = int.from_bytes(self.bytes[:4])
        self.bytes = self.bytes[4:]
        return ret

    def parseString(self) -> str:
        name_length = int.from_bytes(self.bytes[:1])
        string = self.bytes[1:name_length].decode()
        self.bytes = self.bytes[name_length+1:]
        return string

class Reader:
    def __init__(self, library_file: str):
        with open(library_file, "rb") as fp:
            self.data = BytesIO(fp.read())

    def valid(self) -> bool:
        return self.data.readable()
    
    def position(self) -> int:
        return self.data.tell()
    
    # Dynamic sized number
    # If MSB of byte is set shift next byte into it's place
    # Crazy work honestly guys just use a u32 it's not that deep
    def readDynamic(self) -> int:
        loop = self.readU8()
        ret = loop & 0x7F
        offset = 7
        while loop & 0x80:
            loop = self.readU8()
            byte = loop & 0x7F
            ret = ret | (byte << offset)
            offset += 7
        return ret
    
    def read(self, count: int) -> BytesReader:
        return BytesReader(self.data.read(count))
    
    def readU8(self) -> int:
        return int.from_bytes(self.data.read(1))
    
    def peekU8(self, offset) -> int:
        ret = int.from_bytes(self.data.read(1 + offset)[-1:])
        self.data.seek(-1 - offset, os.SEEK_CUR)
        return ret
    
    def peekDynamic(self, initial_next) -> int:
        loop = self.peekU8(initial_next)
        ret = loop & 0x7F
        offset = 7
        next = 1
        while loop & 0x80:
            loop = self.peekU8(initial_next + next)
            byte = loop & 0x7F
            ret = ret | (byte << offset)
            offset += 7
            next += 1
        return ret
    
    def readU16(self) -> int:
        return int.from_bytes(self.data.read(2))
    
    def readU32(self) -> int:
        return int.from_bytes(self.data.read(4))
    
    def readString(self) -> str:
        return self.data.read(self.readU8()).decode()
    
    def readStringLength(self, length: int) -> str:
        return self.data.read(length).decode()