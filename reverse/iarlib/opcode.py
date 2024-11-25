from iarlib.reader import Reader
from iarlib.symbol import Symbol
from iarlib.segment import Segment

def getAbs8(data: Reader):
    if data.peekU8(0) == 0x36:
        data.readU8()
        return data.readU8()
    else:
        raise LookupError("Opcode requested Abs8 but it did not exist")

# Shortcut the Pushes
def getSymbol(data: Reader):
    if data.peekU8(0) == 0x5D:
        symbol = Symbol.getExternal(data.peekDynamic(1))
        if symbol is None:
            raise LookupError("Looked up symbol but got None")
        data.readU8()
        data.readDynamic()
        data.readU32() # Unknown
        return symbol
    elif data.peekU8(0) == 0x5E:
        symbol = Symbol.getRelocatable(data.peekDynamic(1))
        if symbol is None:
            raise LookupError("Looked up symbol but got None")
        data.readU8()
        data.readDynamic()
        data.readU32() # Unknown
        return symbol
    else:
        raise LookupError("Opcode requested Symbol but it did not exist")
    
def reprAbsOrSymbol(value):
    if type(value) == int:
        return f'#{value:02X}h'
    else:
        return f'{value!r}'

def getAbsOrSymbol(data: Reader):
    try:
        return getAbs8(data)
    except:
        return getSymbol(data)

# Label?
class Addr11:
    def __repr__(self):
        return f'{self.value!r}'
    def __init__(self, data: Reader):
        self.value = getSymbol(data)

# Label?
class Addr16:
    def __repr__(self):
        return f'{self.value!r}'
    def __init__(self, data: Reader):
        self.value = getSymbol(data)

class NotBit:
    def __repr__(self):
        return f'/{self.value:02X}h'
    def __init__(self, data: Reader):
        self.value = getAbs8(data)

class Bit:
    def __repr__(self):
        return f'{self.value:02X}h'
    def __init__(self, data: Reader):
        self.value = getAbs8(data)

class Direct:
    def __repr__(self):
        return reprAbsOrSymbol(self.value)
    def __init__(self, data: Reader):
        self.value = getAbsOrSymbol(data)
        
class Immediate:
    def __repr__(self):
        return reprAbsOrSymbol(self.value)
    def __init__(self, data: Reader):
        self.value = getAbsOrSymbol(data)

# Label?
class Offset:
    def __repr__(self):
        if isinstance(self.value, Segment):
            return f'{self.value!r} + {self.offset}'
        else:
            return reprAbsOrSymbol(self.value)
    def __init__(self, data: Reader):
        try:
            self.value = getAbsOrSymbol(data)
        except:
            data.readU8()
            self.value = Segment.get(data.readDynamic())
            self.offset = data.readU32()
        
class Indirect:
    def __repr__(self):
        return f'@R{self.value}'
    def __init__(self, op):
        self.value = op & 0x01
        
class Register:
    def __repr__(self):
        return f'R{self.value}'
    def __init__(self, op):
        self.value = op & 0x07
        
# OPCODES

class ACALL:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = Addr11()

class ADD:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x24:
            self.params = ["A", Immediate(data)]
        elif op == 0x25:
            self.params = ["A", Direct(data)]
        elif (op & 0xFE) == 0x26:
            self.params = ["A", Indirect(op)]
        elif (op & 0xF8) == 0x28:
            self.params = ["A", Register(op)]

class ADDC:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x34:
            self.params = ["A", Immediate(data)]
        elif op == 0x35:
            self.params = ["A", Direct(data)]
        elif (op & 0xFE) == 0x36:
            self.params = ["A", Indirect(op)]
        elif (op & 0xF8) == 0x38:
            self.params = ["A", Register(op)]

class AJMP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = Addr11()

class ANL:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x52:
            self.params = [Direct(data), "A"]
        elif op == 0x53:
            self.params = [Direct(data), Immediate(data)]
        elif op == 0x54:
            self.params = ["A", Immediate(data)]
        elif op == 0x55:
            self.params = ["A", Direct(data)]
        elif op == 0x82:
            self.params = ["C", Bit(data)]
        elif op == 0xB0:
            self.params = ["C", NotBit(data)]
        elif (op & 0xFE) == 0x56:
            self.params = ["A", Indirect(op)]
        elif (op & 0xF8) == 0x58:
            self.params = ["A", Register(op)]

class CJNE:
    def __init__(self, data: Reader):
        op = data.readU8()
        if (op & 0xFE) == 0xB6:
            self.params = [Indirect(op), Immediate(data), Offset(data)]
        elif op == 0xB4:
            self.params = ["A", Immediate(data), Offset(data)]
        elif op == 0xB5:
            self.params = ["A", Direct(data), Offset(data)]
        elif (op & 0xF8) == 0xB8:
            self.params = [Register(op), Immediate(data), Offset(data)]

class CLR:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0xE4:
            self.params = ["A"]
        elif op == 0xC2:
            self.params = [Bit(data)]
        elif op == 0xC3:
            self.params = ["C"]

class CPL:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0xF4:
            self.params = ["A"]
        elif op == 0xB2:
            self.params = [Bit(data)]
        elif op == 0xB3:
            self.params = ["C"]

class DA:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["A"]

class DEC:
    def __init__(self, data: Reader):
        op = data.readU8()
        if (op & 0xFE) == 0x16:
            self.params = [Indirect(op)]
        elif op == 0x14:
            self.params = ["A"]
        elif op == 0x15:
            self.params = [Direct(data)]
        elif (op & 0xF8) == 0x18:
            self.params = [Register(op)]

class DIV:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["AB"]

class DJNZ:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0xD5:
            self.params = [Direct(data), Offset(data)]
        elif (op & 0xF8) == 0xD8:
            self.params = [Register(op), Offset(data)]

class INC:
    def __init__(self, data: Reader):
        op = data.readU8()
        if (op & 0xFE) == 0x06:
            self.params = [Indirect(op)]
        elif op == 0x04:
            self.params = ["A"]
        elif op == 0x05:
            self.params = [Direct(data)]
        elif op == 0xA3:
            self.params = ["DPTR"]
        elif (op & 0xF8) == 0x08:
            self.params = [Register(op)]

class JB:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Bit(data), Offset(data)]

class JBC:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Bit(data), Offset(data)]

class JC:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Offset(data)]

class JMP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["@A+DPTR"]

class JNB:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Bit(data), Offset(data)]

class JNC:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Offset(data)]

class JNZ:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Offset(data)]

class JZ:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Offset(data)]

class LCALL:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Addr16(data)]

class LJMP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Addr16(data)]

class MOV:
    def __init__(self, data: Reader):
        op = data.readU8()
        if (op & 0xFE) == 0x76:
            self.params = [Indirect(op), Immediate(data)]
        elif (op & 0xFE) == 0xF6:
            self.params = [Indirect(op), "A"]
        elif (op & 0xFE) == 0xA6:
            self.params = [Indirect(op), Direct(data)]
        elif op == 0x74:
            self.params = ["A", Immediate(data)]
        elif (op & 0xFE) == 0xE6:
            self.params = ["A", Indirect(op)]
        elif op == 0xE5:
            self.params = ["A", Direct(data)]
        elif (op & 0xF8) == 0xE8:
            self.params = ["A", Register(op)]
        elif op == 0x92:
            self.params = [Bit(data), "C"]
        elif op == 0xA2:
            self.params = ["C", Bit(data)]
        elif op == 0x85:
            self.params = [Direct(data), Direct(data)]
        elif op == 0x75:
            self.params = [Direct(data), Immediate(data)]
        elif (op & 0xFE) == 0x86:
            self.params = [Direct(data), Indirect(op)]
        elif op == 0xF5:
            self.params = [Direct(data), "A"]
        elif (op & 0xF8) == 0x88:
            self.params = [Direct(data), Register(op)]
        elif op == 0x90:
            self.params = ["DPTR", Immediate(data)]
        elif (op & 0xF8) == 0x78:
            self.params = [Register(op), Immediate(data)]
        elif (op & 0xF8) == 0xF8:
            self.params = [Register(op), "A"]
        elif (op & 0xF8) == 0xA8:
            self.params = [Register(op), Direct(data)]

class MOVC:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x93:
            self.params = ["A", "@A+DPTR"]
        elif op == 0x83:
            self.params = ["A", "@A+PC"]

class MOVX:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0xF0:
            self.params = ["@DPTR", "A"]
        elif (op & 0xFE) == 0xF2:
            self.params = [Indirect(op), "A"]
        elif op == 0xE0:
            self.params = ["A", "@DPTR"]
        elif (op & 0xFE) == 0xE2:
            self.params = ["A", Indirect(op)]

class MUL:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["AB"]

class NOP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = []

class ORL:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x44:
            self.params = ["A", Immediate(data)]
        elif (op & 0xFE) == 0x46:
            self.params = ["A", Indirect(op)]
        elif op == 0x45:
            self.params = ["A", Direct(data)]
        elif (op & 0xF8) == 0x48:
            self.params = ["A", Register(op)]
        elif op == 0xA0:
            self.params = ["C", NotBit(data)]
        elif op == 0x72:
            self.params = ["C", Bit(data)]
        elif op == 0x43:
            self.params = [Direct(data), Immediate(data)]
        elif op == 0x42:
            self.params = [Direct(data), "A"]

class POP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Direct(data)]

class PUSH:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Direct(data)]

class RET:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = []

class RETI:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = []

class RL:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["A"]

class RLC:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["A"]

class RR:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["A"]

class RRC:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["A"]

class SETB:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0xD2:
            self.params = [Bit(data)]
        elif op == 0xD3:
            self.params = ["C"]

class SJMP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = [Offset(data)]

class SUBB:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x94:
            self.params = ["A", Immediate(data)]
        elif (op & 0xFE) == 0x96:
            self.params = ["A", Indirect(op)]
        elif op == 0x95:
            self.params = ["A", Direct(data)]
        elif (op & 0xFE) == 0x98:
            self.params = ["A", Register(op)]

class SWAP:
    def __init__(self, data: Reader):
        data.readU8()
        self.params = ["A"]

class XCH:
    def __init__(self, data: Reader):
        op = data.readU8()
        if (op & 0xFE) == 0xC6:
            self.params = ["A", Indirect(op)]
        elif op == 0xC5:
            self.params = ["A", Direct(data)]
        elif (op & 0xF8) == 0xC8:
            self.params = ["A", Register(op)]

class XCHD:
    def __init__(self, data: Reader):
        op = data.readU8()
        self.params = ["A", Indirect(op)]

class XRL:
    def __init__(self, data: Reader):
        op = data.readU8()
        if op == 0x64:
            self.params = ["A", Immediate(data)]
        elif (op & 0xFE) == 0x66:
            self.params = ["A", Indirect(op)]
        elif op == 0x65:
            self.params = ["A", Direct(data)]
        elif (op & 0xF8) == 0x68:
            self.params = ["A", Register(op)]
        elif op == 0x63:
            self.params = [Direct(data), Immediate(data)]
        elif op == 0x62:
            self.params = [Direct(data), "A"]

# Not defined by spec
class UNDEF:
    def __init__(self, data: Reader):
        data.readU8()

# Key on 4 MSB, val index on 4 LSB (last fills row)
encodings = {
    0x00: [NOP, AJMP, LJMP, RR, INC],
    0x10: [JBC, ACALL, LCALL, RRC, DEC],
    0x20: [JB, AJMP, RET, RL, ADD],
    0x30: [JNB, ACALL, RETI, RLC, ADDC],
    0x40: [JC, AJMP, ORL],
    0x50: [JNC, ACALL, ANL],
    0x60: [JZ, AJMP, XRL],
    0x70: [JNZ, ACALL, ORL, JMP, MOV],
    0x80: [SJMP, AJMP, ANL, MOVC, DIV, MOV],
    0x90: [MOV, ACALL, MOV, MOVC, SUBB],
    0xA0: [ORL, AJMP, MOV, INC, MUL, UNDEF, MOV],
    0xB0: [ANL, ACALL, CPL, CPL, CJNE],
    0xC0: [PUSH, AJMP, CLR, CLR, SWAP, XCH],
    0xD0: [POP, ACALL, SETB, SETB, DA, DJNZ, XCHD, XCHD, DJNZ],
    0xE0: [MOVX, AJMP, MOVX, MOVX, CLR, MOV],
    0xF0: [MOVX, ACALL, MOVX, MOVX, CPL, MOV],
}

class OpCode:
    def __repr__(self):
        return f'\t{self.op.__class__.__name__.lower()} {self.op.params}'.replace('[', '').replace(']', '').replace('\'', '')
    def __init__(self, data: Reader):
        opcode = data.peekU8(0)
        row = opcode & 0xF0
        col = opcode & 0x0F
        cols = encodings[row]
        if col < len(cols):
            self.op = cols[col](data)
        else:
            self.op = cols[-1](data)
        print(self)