from iarlib.reader import Reader, BytesReader
from iarlib.callframeinstruction import CallFrameInstruction

class StackOnColumn:
    def __repr__(self):
        return f'stack based on column {self.column}'
    def __init__(self, bytes: BytesReader):
        self.column = bytes.parseU8()
        self.type = bytes.parseU8()

class StaticOverlay:
    def __repr__(self):
        return f'static overlay frame in segment "{self.name}"'
    def __init__(self, bytes: BytesReader):
        self.name = bytes.parseString()

class BaseAddress:
    # "base address in segment type {type}"
    def __init__(self, bytes: BytesReader):
        print("Base Address frame type not yet implemented")
        exit() # TODO

frame_type_map = {
    0x00: StackOnColumn,
    0x01: StaticOverlay,
    0x02: BaseAddress,
}

class Names1:
    def __init__(self, bytes: BytesReader):
        self.id = bytes.parseU8()
        self.fmtver = bytes.parseU8()
        bytes.parseU8() # Unknown
        default_bits = bytes.parseU8()
        frame_count = bytes.parseU8()
        self.frames = []
        for _ in range(frame_count):
            self.frames.append(frame_type_map[bytes.parseU8()](bytes))

        column_count = bytes.parseU8()
        bytes.parseU32() # Unknown
        bytes.parseU32() # Unknown

        virtual_column_count = bytes.parseU8()
        self.virtual_columns = []
        for _ in range(virtual_column_count):
            self.virtual_columns.append(bytes.parseU8())

        self.columns = []
        for _ in range(column_count):
            column = bytes.parseString()
            has_bits = bytes.peekU8(1) < 0x20
            if has_bits:
                self.columns.append((column, bytes.parseU8()))
            else:
                self.columns.append((column, default_bits))
        
        self.column_components = {}
        component_count = bytes.parseU8()
        while (component_count != 0):
            owner = bytes.parseU8() # Column
            components = []
            for _ in range(component_count):
                components.append(bytes.parseU8()) # Column
            self.column_components[owner] = components
            component_count = bytes.parseU8()

class Common:
    def __init__(self, bytes: BytesReader):
        self.id = bytes.parseU8()
        self.version = bytes.parseU8()
        self.name = bytes.parseString()
        self.code_align = bytes.parseU8()
        self.data_align = bytes.parseU8()
        self.return_address = bytes.parseU8() # Column
        bytes.parseU8() # Unknown
        bytes.parseU8() # Unknown
        self.names_index = bytes.parseU8() # Call frame not name table
        self.instructions = []
        while bytes.valid():
            self.instructions.append(CallFrameInstruction(bytes))
        
class Data:
    def __init__(self, bytes: BytesReader):
        self.common = bytes.parseU8()
        self.tot = bytes.parseU8()
        bytes.parseU8() # Unknown

type_map = {
    # 0x01: Names,
    0x02: Common,
    0x03: Data,
    0x05: Names1,
    # 0x06: Data1,
    # 0x07: CommonE,
}

class CallFrame:
    ID = 0xD4
    def __init__(self, data: Reader):
        byte_count = data.readDynamic()
        bytes = data.read(byte_count)
        self.sub = type_map[bytes.parseU8()](bytes)