import os
from io import BytesIO

class Reader:
    def __init__(self, library_file: str):
        with open(library_file, "rb") as fp:
            self.data = BytesIO(fp.read())

    def valid(self) -> bool:
        return self.data.readable()
    
    def position(self) -> int:
        return self.data.tell()
    
    def readU8(self) -> int:
        return int.from_bytes(self.data.read(1))
    
    def peekU8(self, offset) -> int:
        ret = int.from_bytes(self.data.read(1 + offset)[-1:])
        self.data.seek(-1 - offset, os.SEEK_CUR)
        return ret
    
    def readU16(self) -> int:
        return int.from_bytes(self.data.read(2))
    
    def readU32(self) -> int:
        return int.from_bytes(self.data.read(4))
    
    def readString(self) -> str:
        return self.data.read(self.readU8()).decode("utf-8")
    
    def readStringLength(self, length: int) -> str:
        return self.data.read(length).decode("utf-8")