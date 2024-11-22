from iarlib.reader import Reader
from iarlib.callframeinstruction import CallFrameInstruction

import time

class StackOnColumn:
    def __repr__(self):
        return f'stack based on column {self.column}'
    def __init__(self, data: Reader):
        self.column = data.readU8()
        self.type = data.readU8()

class StaticOverlay:
    def __repr__(self):
        return f'static overlay frame in segment "{self.name}"'
    def __init__(self, data: Reader):
        self.name = data.readString()

class BaseAddress:
    # "base address in segment type {type}"
    def __init__(self, data: Reader):
        print("Base Address frame type not yet implemented")
        exit() # TODO

frame_type_map = {
    0x00: StackOnColumn,
    0x01: StaticOverlay,
    0x02: BaseAddress,
}

class Names1:
    def __init__(self, byte_count, data: Reader):
        fmtver = data.readU8()
        data.readU8() # Unknown
        default_bits = data.readU8()
        frame_count = data.readU8()
        self.frames = []
        for _ in range(frame_count):
            self.frames.append(frame_type_map[data.readU8()](data))

        column_count = data.readU8()
        data.readU32() # Unknown
        data.readU32() # Unknown

        virtual_column_count = data.readU8()
        self.virtual_columns = []
        for _ in range(virtual_column_count):
            self.virtual_columns.append(data.readU8())

        self.columns = []
        for _ in range(column_count):
            column = data.readString()
            has_bits = data.peekU8(1) < 0x20
            if has_bits:
                self.columns.append((column, data.readU8()))
            else:
                self.columns.append((column, default_bits))
        
        self.column_components = {}
        component_count = data.readU8()
        while (component_count != 0):
            owner = data.readU8() # Column
            components = []
            for _ in range(component_count):
                components.append(data.readU8()) # Column
            self.column_components[owner] = components
            component_count = data.readU8()

class Common:
    def __init__(self, byte_count, data: Reader):
        self.name = data.readString()
        self.code_align = data.readU8()
        self.data_align = data.readU8()
        self.return_address = data.readU8() # Column
        data.readU8() # Unknown
        data.readU8() # Unknown
        self.names_index = data.readU8() # Call frame not name table
        end_address = data.position() + byte_count - (len(self.name) + 10)
        self.instructions = []
        while data.position() < end_address:
            self.instructions.append(CallFrameInstruction(data))
        

type_map = {
    0x00: Names1,
    0x01: Common,
}

class CallFrame:
    def ID():
        return 0xD4
    def __init__(self, data: Reader):
        byte_count = data.readU8()
        data.readU8() # Unknown
        self.index = data.readU8()
        self.sub = type_map[data.readU8()](byte_count, data)