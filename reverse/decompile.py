#!/usr/bin/env python3

import sys
import getopt
from pprint import pprint
from iarlib.reader import Reader
section_type = {}

from iarlib.library import *
section_type[Library.ID] = Library
section_type[Auxillary.ID] = Auxillary
section_type[Auxillary1.ID] = Auxillary1
section_type[Version.ID] = Version
section_type[End.ID] = End
from iarlib.keyvalue import KeyValue
section_type[KeyValue.ID] = KeyValue
from iarlib.memoryinfo import MemoryInfo
section_type[MemoryInfo.ID] = MemoryInfo
from iarlib.attribute import Attribute
section_type[Attribute.ID] = Attribute
from iarlib.nametable import NameTable
section_type[NameTable.ID] = NameTable
from iarlib.pointertype import PointerType
section_type[PointerType.ID] = PointerType
from iarlib.type import Type
section_type[Type.ID] = Type
from iarlib.sizetype import SizeType
section_type[SizeType.ID] = SizeType
from iarlib.segment import Segment
section_type[Segment.ID] = Segment
from iarlib.callframe import CallFrame
section_type[CallFrame.ID] = CallFrame
from iarlib.symbol import Symbol, SourceCall
section_type[Symbol.ID] = Symbol
section_type[SourceCall.ID] = SourceCall
from iarlib.instruction import *
section_type[OrgRel.ID] = OrgRel
section_type[AssemblyMode.ID] = AssemblyMode
section_type[PushExt.ID] = PushExt
section_type[DeleteTos.ID] = DeleteTos
section_type[Abs8.ID] = Abs8
section_type[Abs16.ID] = Abs16
section_type[Pop8.ID] = Pop8
section_type[PushRel.ID] = PushRel
section_type[PushAbs.ID] = PushAbs
section_type[PushPcr.ID] = PushPcr
section_type[Minus.ID] = Minus
section_type[Pop24.ID] = Pop24
from iarlib.error import *
section_type[StackError.ID] = StackError
section_type[Check.ID] = Check
section_type[Copy.ID] = Copy
section_type[LSR.ID] = LSR

try:
    options, values = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    for opt, val in options:
        if opt in ("-h", "--help"):
            print ("Usage: decompile.py [--help] [--output=] <lib>")
            exit()
        elif opt in ("-o", "--output"):
            print ("Output:", val)
        else:
            print ("Unknown option: ", opt)
            exit()
    
    if len(values) > 1 or len(values) == 0:
        print ("Specify one library to process!")
        exit()
    print ("Processing: ", values)
except getopt.error as error:
    print(error)

data = Reader(values[0])

sections = []
while (data.valid()):
    section_id = data.readU8()
    if section_type.get(section_id) is not None:
        sections.append(section_type[section_id](data))
    elif section_id == 0xFF:
        print("Successfully read file")
        break
    else:
        pprint(sections)
        print(f"Unknown section ID: {section_id:02X}")
        exit(1)



print("Exiting...")