from iarlib.reader import Reader

key_values = {}

class KeyValue:
    def ID():
        return 0xC9
    
    def __init__(self, data: Reader):
        global key_values
        data.readU32() # Size, ignore
        length = data.readU32()
        key = data.readStringLength(length)
        length = data.readU32()
        value = data.readStringLength(length)
        key_values[key] = value
