from iarlib.reader import Reader

class Offset:
    def __init__(self, column, data: Reader):
        self.column = column
        self.offset = data.readU8()

class Undefined:
    def __init__(self, data: Reader):
        self.column = data.readU8()

class SameValue:
    def __init__(self, data: Reader):
        self.column = data.readU8()

class DefaultCallFrameAddress:
    def __init__(self, data: Reader):
        self.column = data.readU8()
        self.offset = data.readU8()

class IAR_DefaultCallFrameAddressInstruction:
    def __init__(self, data: Reader):
        data.readU8() # Unknown
        self.column = data.readU8()
        self.offset = data.readU8()

class IAR_DefaultCallFrameAddressInstructionStaticOverlay:
    def __init__(self, data: Reader):
        self.frame = data.readU8()

call_frame_instruction_map = {
    # 0x01: SetLocation,
    # 0x02: AdvanceLocation1,
    # 0x03: AdvanceLocation2,
    # 0x04: AdvanceLocation4,
    # 0x05: OffsetExtended,
    # 0x06: RemoteExtended,
    0x07: Undefined,
    0x08: SameValue,
    # 0x09: Register,
    # 0x0A: RememberState,
    # 0x0B: RestoreState,
    0x0C: DefaultCallFrameAddress,
    # 0x0D: DefaultCallFrameAddressRegister,
    # 0x0E: DefaultCallFrameAddressOffset,
    # 0x0F: DefaultCallFrameAddressExpression,
    # 0x10: Expression,
    # 0x11: OffsetExtendedSF,
    # 0x12: DefaultCallFrameAddressSF,
    # 0x13: DefaultCallFrameAddressOffsetSF,
    # 0x14: ValueOffset,
    # 0x15: ValueOffset2,
    # 0x16: ValueExpression,
    0x1C: IAR_DefaultCallFrameAddressInstruction,
    # 0x1D: IAR_DefaultCallFrameAddressRegister,
    # 0x1E: IAR_DefaultCallFrameAddressInstructionOffset,
    0x1F: IAR_DefaultCallFrameAddressInstructionStaticOverlay,
    # 0x20: IAR_OffsetInstructionExtended,
    # 0x21: IAR_Valid,
    # 0x22: IAR_Invalid,
    # 0x23: IAR_DefaultCallFrameAddressExpression,
    # 0x24: IAR_Expression,
    # 0x25: IAR_DefaultCallFrameAddressInstructionNotUsed,
}

class CallFrameInstruction:
    def __repr__(self):
        return f'{self.instruction}'
    def __init__(self, data: Reader):
        type = data.readU8()
        if type > 128 and type < 192:
            # Special case? Type is column index
            self.instruction = Offset(type - 128, data)
        else:
            self.instruction = call_frame_instruction_map[type](data)
