#pragma endian big

import std.mem;
import std.io;

struct MapEntry {
    // 8 larger than key + val because it includes u32 sizes
    u32 size;
 
    u32 nameLength;
    char name[nameLength];
    
    u32 valLength;
    char val[valLength];
}[[sealed]];

struct DataAttrEntry {
    u16 size;
    
    u32 unk;
    
    u32 nameLength;
    char name[nameLength];
};

struct CallConvEntry {
    u16 size;
    
    u16 unk;
    
    u8 nameLength;
    char name[nameLength];
};

struct SymbolEntry {
    u32 size;
    
    u32 unk; //Count?
    
    u8 nameLength;
    char name[nameLength];
    
    u32 pad; //0xFF
};

struct CodeEntry {
    char name[0]; // Has to exist
    
    u32 unk1; // 06 06 06 06
    u8 unk2; // 15
    
};

enum EntryType: u8 {
    Map = 0xC9,
    DataAttr = 0xC6,
    CallConv = 0xD3,
    Symbol = 0xCD,
    Code = 0xC1,
};

struct Entry {
    EntryType type;
    match (type) {
        (EntryType::Map): MapEntry e;
        (EntryType::DataAttr): DataAttrEntry e;
        (EntryType::CallConv): CallConvEntry e;
        (EntryType::Symbol): SymbolEntry e;
        (EntryType::Code): CodeEntry e;
    }
} [[name(e.name), format("Entry_formatValue")]];

fn Entry_formatValue (auto entry) {
    match (entry.type) {
        (EntryType::Map): return entry.e.val;
        (EntryType::DataAttr): return std::format("{:08X}", entry.e.unk);
        (EntryType::CallConv): return std::format("{:04X}", entry.e.unk);
        (EntryType::Symbol): return std::format("{:08X}", entry.e.unk);
        (_): return null;
    }
};

fn Entry_valid () {
    EntryType type = std::mem::read_unsigned($, 1);
    match (type) {
        (EntryType::Map): return true;
        (EntryType::DataAttr): return true;
        (EntryType::CallConv): return true;
        (EntryType::Symbol): return true;
        (EntryType::Code): return true;
        (_): return false;
    }
};

struct IARHeader {
    u8 unk1[7];
    
    u8 fileNameLength;
    char fileName[fileNameLength];
    
    u8 unk2[11];
    
    u8 compilerVersionLength;
    char compilerVersion[compilerVersionLength];
    
    Entry entrys[while(Entry_valid())];
};

struct IARFile {
    IARHeader header;
} [[name(header.fileName)]];


IARFile file @ 0x00;