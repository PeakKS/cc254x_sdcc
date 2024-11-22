#pragma endian big

import std.mem;
import std.io;
import std.core;

struct FileHeader {
    u8 pad;
    u8 rev;
    u8 cpa;
    u8 year;
    u8 day;
    u8 month;
    u8 unk1;
    
    u8 fileNameLength;
    char fileName[fileNameLength];
    
    u8 unk2;
    u8 major;
    u8 minor;
    u8 revision;
      
    u8 unk3[7];
    
    u8 compilerVersionLength;
    char compilerVersion[compilerVersionLength];
};

struct KeyValue {
    u8 type[[hidden]];
    u32 size;
 
    u32 nameLength;
    char name[nameLength];
    
    u32 valLength;
    char val[valLength];
} [[name(name)]];

enum Intrinsic: u8 {
    UnsignedChar = 0x01,
    SignedChar = 0x02,
    UnsignedShort = 0x03,
    SignedShort = 0x04,
    UnsignedInt = 0x05,
    SignedInt = 0x06,
    UnsignedLong = 0x07,
    SignedLong = 0x08,
};

struct MemInfo {
    u8 type[[hidden]];
    u16 size;
    
    u8 index;
    u8 ptr_size;
    Intrinsic intrinsic;
    u8 flags;
    
    u32 nameLength;
    char name[nameLength];
} [[name(name)]];

struct AttrName {
    u8 type[[hidden]];
    u16 size;
    
    u16 unk;
    
    u8 nameLength;
    char name[nameLength];
} [[name(name)]];

struct ScopedName {
    u8 type[[hidden]];
    u32 size;
    
    u32 unk; //Count?
    
    u8 nameLength;
    char name[nameLength];
    
    u32 nameIndex; // Ref to other scoped name, 0xFF if none
} [[name(name)]];

fn GetScopedName(ref ScopedName nameTable, u32 nameIndex) {
    if (nameIndex == 0xFFFFFFFF)   
        return null;

    str name = nameTable[nameIndex].name;
    u32 refIndex = nameTable[nameIndex].nameIndex;
    while (refIndex != 0xFFFFFFFF) {
        name = nameTable[refIndex].name + name;
        refIndex = nameTable[refIndex].nameIndex;
    }
    
    return name;
};

struct DefPtrType {
    u8 type[[hidden]];
    // Index into MemInfo
    u8 staticData;
    u8 autoData;
    u8 constData;
    u8 generalData;
    u8 code;
};

struct DynamicNumber {
    u8 first;
    u8 next[while (std::mem::read_unsigned($-1, 1) & 0x80)];
};

fn DynamicNumberValue(DynamicNumber d) {
    u32 ret = d.first & 0x7F;
    for (u32 idx = 0, idx < std::core::member_count(d.next), idx = idx + 1) {
        ret |= ((d.next[idx] & 0x7F) << (7 * (idx + 1)));
    }
    return ret;
};

struct TypeRef {
    DynamicNumber dyn;
} [[format("GetTypeRefName")]];

fn GetTypeRefName(TypeRef typeRef) {
    match (typeRef.dyn.first) {
        (Intrinsic::UnsignedChar): return "unsigned char";
        (Intrinsic::SignedChar): return "signed char";
        (Intrinsic::UnsignedShort): return "unsigned short";
        (Intrinsic::SignedShort): return "signed short";
        (Intrinsic::UnsignedInt): return "unsigned int";
        (Intrinsic::SignedInt): return "signed int";
        (Intrinsic::UnsignedLong): return "unsigned long";
        (Intrinsic::SignedLong): return "signed long";
        (_): return "reference";
    }
};

struct Pointer {
    TypeRef typeRef;
};

struct Function {
    TypeRef retType;
    u8 format; //ANSI ?
    u8 paramCount;
    TypeRef params[paramCount];
};

struct Array {
    TypeRef typeRef;
    u32 size;
    u32 count;
};

struct DataAttr {
    u8 memInfoRef;
    TypeRef typeRef;
    u32 gen;
    u8 unk; // type for next? 0x04 = target?
    u32 target;
};

struct FuncAttr {
    u8 memInfoRef;
    TypeRef typeRef;
    u32 gen; //??? 8 = prototyped?
    u8 unk;
    u32 target;
    
};

struct Typedef {
    TypeRef typeRef;
    u32 nameIndex;
};

struct StructUnionMember {
    u32 index;
    u32 nameIndex;
    TypeRef typeRef;
    u32 unk; // Init?
} [[name(GetScopedName(parent.parent.parent.scopedNames, nameIndex))]];

struct StructUnion {
    u32 nameIndex;
    u32 dataType; // 9 = struct? ? = union?
    u32 bytes;
    u32 count;
    StructUnionMember members[count];
};

enum TypeKind: u8 {
    Pointer = 0x0F,
    Function = 0x14,
    Array = 0x29,
    DataAttr = 0x2A,
    FuncAttr = 0x2B,
    Typedef = 0x31,
    StructUnion = 0x34,
};

struct Type {
    u8 type[[hidden]];
    TypeRef typeRef; // Others mention this struct by this
    
    TypeKind kind;
    match (kind) {
        (TypeKind::Pointer): Pointer internal;
        (TypeKind::Function): Function internal;
        (TypeKind::Array): Array internal;
        (TypeKind::DataAttr): DataAttr internal;
        (TypeKind::FuncAttr): FuncAttr internal;
        (TypeKind::Typedef): Typedef internal;
        (TypeKind::StructUnion): StructUnion internal;
    }
} [[name(Type_GetName(kind, internal))]];

fn Type_GetName(auto type, auto internal) {
    match (type) {
        (TypeKind::Typedef): return GetScopedName(internal.parent.parent.scopedNames, internal.nameIndex);
        (TypeKind::StructUnion): return GetScopedName(internal.parent.parent.scopedNames, internal.nameIndex);
        (_): return null;
    }
};

enum SizeTypeType: u8 {
    UnsignedChar = 0x01,
    SignedChar = 0x02,
    UnsignedShort = 0x03,
    Short = 0x04,
    UnsignedInt = 0x05,
    Int = 0x06,
    UnsignedLong = 0x07,
    Long = 0x08,
    Float = 0x09,
    Double = 0x0A,
    LongDouble = 0x0B,
    UnsignedLongLong = 0x2D,
    LongLong = 0x2E,
    Bool = 0x2F,
    Wchar = 0x30,
    CharUnsigned = 0x36, // Why?
};

struct SizeType {
    u8 type[[hidden]];
    SizeTypeType sizeType;
    u8 size;
} [[name(sizeType), format("GetSizeTypeName")]];

fn GetSizeTypeName(auto sizeType) {
    return sizeType.size;
};

enum SegmentType: u8 {
    CODE = 0x21,
    DATA = 0x22,
    XDATA = 0x23,
    IDATA = 0x24,
};

// No idea what this means
enum SPAType: u8 {
    None = 0x80, // Displays as 00
    Reorder = 0xA0, // Displays as 20
};

struct Segment {
    u8 type[[hidden]];
    SPAType spaType;
    u8 index; //Unsure but unique
    SegmentType segmentType;
    u8 nameLength;
    char name[nameLength];
} [[name(name)]];

enum FrameType: u8 {
    StackBasedOnCall = 0,
    StaticOverlayFrame = 1,
    BaseAddressInSegType = 2,
};

struct StackBasedFrame {
    u8 column;
    u8 type;
};

struct StaticOverlayFrame {
    u8 nameLength;
    char name[nameLength];
};

struct Frame {
    FrameType frameType;
    match (frameType) {
        (FrameType::StackBasedOnCall): StackBasedFrame;
        (FrameType::StaticOverlayFrame): StaticOverlayFrame;
    }
};

struct Column {
    u8 nameLength;
    char name[nameLength];
    // Assume name length is less than lowest valid string char
    // If no bits member size is parent.defaultBitCount
    if (std::mem::read_unsigned($+1, 1) < 0x20) {
        u8 bitCount;
    }
} [[name(name)]];

struct ColumnComponents {
    u8 compCount;
    u8 owner;
    u8 components[compCount];
};

struct CallFrameNames1 {
    u8 id;
    u8 fmtVer;
    u16 defaultBitCount;
    u8 frameCount;
    Frame frames[frameCount];
    
    u8 colCount;
    u8 unk2[8];
    u8 virtualColCount;
    u8 virualCols[virtualColCount];
    Column cols[colCount];
    
    ColumnComponents colComps[3];
    u8 unk3;
};

struct CFA_Undefined {
    u8 column;
};

struct CFA_SameValue {
    u8 column;
};

struct CFA_Default {
    u8 column;
    u8 offset; // Negative
};

struct CFA_StaticOverlay {
    u8 frame;
};

struct CFA_IAR_Default {
    u8 unk;
    u8 column;
    u8 offset;
};

struct CFA_Offset {
    //u8 column; get from parent // Subtract 128
    u8 offset;
};

enum CFA_Type: u8 {
    Undefined = 0x07,
    SameValue = 0x08,
    Default = 0x0C,
    StaticOverlay = 0x1F,
    IAR_Default = 0x1C,
};

fn CFA_IsOffset(auto type) {
    if ((type > 128) && (type < 192)) // Figure out real upper end of range
        return true;
    else
        return false;
};

fn CFA_Valid() {
    CFA_Type type = std::mem::read_unsigned($, 1);
    match(type) {
        (CFA_Type::Undefined): return true;
        (CFA_Type::SameValue): return true;
        (CFA_Type::Default): return true;
        (CFA_Type::StaticOverlay): return true;
        (CFA_Type::IAR_Default): return true;
        (_): return CFA_IsOffset(type);
    }
    return false;
};

struct CallFrameAddress {
    CFA_Type type;
    match(type) {
        (CFA_Type::Undefined): CFA_Undefined;
        (CFA_Type::SameValue): CFA_SameValue;
        (CFA_Type::Default): CFA_Default;
        (CFA_Type::StaticOverlay): CFA_StaticOverlay;
        (CFA_Type::IAR_Default): CFA_IAR_Default;
        (_): if (CFA_IsOffset(type)) {
            CFA_Offset;
        }
    }
};

struct CallFrameCommon {
    u8 id;
    u8 ver;
    u8 nameLength;
    u8 name[nameLength];
    u8 codeAlign;
    u8 dataAlign; // -128
    u8 returnAddr; // Column IDX
    
    u8 unk[2];
    u8 namesIndex;
    
    CallFrameAddress cfa[while(CFA_Valid())];
};

enum CFIOtherType: u8 {
    SetLoc = 0x01,
    AdvanceLoc1 = 0x02,
    AdvanceLoc2 = 0x03,
    AdvanceLoc4 = 0x04,
    OffsetExtended = 0x05,
    RemoteExtended = 0x06,
    Undefined = 0x07,
    SameValue = 0x08,
    Register = 0x09,
    RememberState = 0x0A,
    RestoreState = 0x0B,
    DefCFA = 0x0C,
    DefCFARegister = 0x0D,
    DefCFAOffset = 0x0E,
    DefCFAExpression = 0x0F,
    Expression = 0x10,
    OffsetExtendedSF = 0x11,
    DefCFASF = 0x12,
    DefCFAOffsetSF = 0x13,
    ValOffset = 0x14,
    ValOffset2 = 0x15,
    ValExpression = 0x16,
    IARDefCFAI = 0x1C,
    IARDefCFARegister = 0x1D,
    IARDefCFAIOffset = 0x1E,
    IARDefCFAStaticIOffset = 0x1F,
    IAROffsetIExtended = 0x20,
    IARValid = 0x21,
    IARInvalid = 0x22,
    IARDefCFAExpression = 0x23,
    IAR_Expression = 0x24,
    IAR_DefCFAINotUsed = 0x25,
};

struct CFIBaseOther {
    CFIOtherType instruction;
    u8 next;
};

struct CFIBaseAdvanceLoc {
    u8 instruction;
};

struct CFIBaseOffset {
    u8 instruction; // Col PTR
    u8 offset;
};

struct CFIBaseRestore {
    u8 instruction; // Col PTR
};

enum CFIBaseType: u8 {
    Other = 0x00,
    AdvanceLoc = 0x40,
    Offset = 0x80,
    Restore = 0xC0,
};

struct CallFrameInstruction {
    match (std::mem::read_unsigned($, 1) & 0xC0) {
        (CFIBaseType::Other): CFIBaseOther;
        (CFIBaseType::AdvanceLoc): CFIBaseAdvanceLoc;
        (CFIBaseType::Offset): CFIBaseOffset;
        (CFIBaseType::Restore): CFIBaseRestore;
    }
};

struct DefCFAOffset {
    u8 ins;
    u8 offset;
};



struct CallFrameIns {
    u8 ins;
}[[name(CallFrameData_Name(ins))]];

struct CallFrameData {
    u8 common;
    u8 TOT;
    u8 unk2;
    u8 ins[DynamicNumberValue(parent.byteCount) - 4];
};

enum CallFrameType: u8 {
    COMMON = 0x02,
    DATA = 0x03,
    NAMES1 = 0x05,
};

struct CallFrame {
    u8 type[[hidden]];
    DynamicNumber byteCount;
    CallFrameType callFrameType;
    match (callFrameType) {
        (CallFrameType::COMMON): CallFrameCommon;
        (CallFrameType::DATA): CallFrameData;
        (CallFrameType::NAMES1): CallFrameNames1;
    }
}[[name(callFrameType)]];

struct SubDefFrameSize {
    u8 type[[hidden]];
    u8 SNO; // sub number?
    u32 size;
    u16 flags;    
};

struct SubDefCount {
    u8 type[[hidden]];
    u32 count;
    SubDefFrameSize frameSizes[count];
};

struct SymbolDef {
    u8 type[[hidden]];
    u8 unk1[5];
    u8 index;
    u8 unk2[7];
    u8 nameIndex;
    TypeRef typeRef;
    u8 unk3[3]; // Location probably
    if (std::mem::read_unsigned($, 1) == 0xB1) {

        u8 funcType[[hidden]];
        u16 funcIndex;
        u32 funcDef;
        
        SubDefCount counts[while(std::mem::read_unsigned($, 1) == 0xC4)];
    } else if (std::mem::read_unsigned($, 1) == 0xB0) {
        u8 funcType[[hidden]];
        u16 funcIndex;
        u16 file;
        u16 line;
        u32 funcDef;
        u8 unk4[2];
        SubDefCount counts[while(std::mem::read_unsigned($, 1) == 0xC4)];
    }
} [[name(std::format("[{}]", index) + GetScopedName(parent.scopedNames, nameIndex))]];

struct OrgRel {
    u8 type[[hidden]];
    u8 unk1;
    u32 unk2;
};

enum AsmMode: u8 {
    CODE1 = 0x01,
    DATA16 = 0x0B,
};

struct AsmModeChange {
    u8 type[[hidden]];
    AsmMode mode;
};

struct PushExt {
    u8 type[[hidden]];
    u8 num;
    u32 unk;
};

struct PushRel {
    u8 type[[hidden]];
    u8 unk1;
    u32 unk2;
};

struct Abs8 {
    u8 type[[hidden]];
    u8 num;
};

struct StackError {
    u8 type[[hidden]];
    u8 errorLength;
    char error[errorLength];
};

struct Check {
    u8 type[[hidden]];
    u32 upper;
    u32 lower;
};

struct Copy {
    u8 type[[hidden]];
};

struct LSR {
    u8 type[[hidden]];
    u32 val;
};

struct Pop8 {
    u8 type;
};

struct IARFile {
    FileHeader header;
    
    KeyValue keyVals[while(std::mem::read_unsigned($, 1) == 0xC9)];
    MemInfo memInfos[while(std::mem::read_unsigned($, 1) == 0xC6)];
    AttrName attrNames[while(std::mem::read_unsigned($, 1) == 0xD3)];
    ScopedName scopedNames[while(std::mem::read_unsigned($, 1) == 0xCD)];
    DefPtrType ptrTypes[while(std::mem::read_unsigned($, 1) == 0xC1)];
    Type types[while(std::mem::read_unsigned($, 1) == 0x4A)];
    SizeType sizeTypes[while(std::mem::read_unsigned($, 1) == 0x4F)];
    Segment segments[while(std::mem::read_unsigned($, 1) == 0x4B)];
    CallFrame callFrames[while(std::mem::read_unsigned($, 1) == 0xD4)];
    SymbolDef symbols[while(std::mem::read_unsigned($, 1) == 0xCE)];
    OrgRel orgRel1; // 0xC7
    AsmModeChange modeChange1; //0xDE
    OrgRel orgRel2; // 0xC7
    PushExt pushExt; // 0x5D
    u8 deleteTos; // 0x9C
    OrgRel orgRel3; // 0xC7
    CallFrame dataFrame;
    AsmModeChange modeChange2;
    Abs8 abs8s[while(std::mem::read_unsigned($, 1) == 0x36)];
    PushRel pushRel; // 0x5E
    StackError error1; // 0x9D
    Check check; // 0x73
    StackError error2; // 0x9D
    Copy copy; // 0x70
    LSR lsr; // 0x6E
    Pop8 pop[2]; // 0x5A
    Abs8 abs8s2[while(std::mem::read_unsigned($, 1) == 0x36)];
    PushExt pushExt2;
    StackError error3;
    u8 ignore[25];
    CallFrame data;
    u8 ignore2[3084];
    CallFrame data2;

} [[name(header.fileName)]];


IARFile file @ 0x00;