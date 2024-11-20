#!/usr/bin/env python3

import sys
import getopt
from pprint import pprint
from iarlib.reader import Reader
section_type = {}

from iarlib.library import Library
section_type[Library.ID()] = Library
from iarlib.library import Auxillary
section_type[Auxillary.ID()] = Auxillary
from iarlib.library import Auxillary1
section_type[Auxillary1.ID()] = Auxillary1
from iarlib.library import Version
section_type[Version.ID()] = Version
from iarlib.keyvalue import KeyValue
section_type[KeyValue.ID()] = KeyValue
from iarlib.memoryinfo import MemoryInfo
section_type[MemoryInfo.ID()] = MemoryInfo
from iarlib.attribute import Attribute
section_type[Attribute.ID()] = Attribute
from iarlib.nametable import NameTable
section_type[NameTable.ID()] = NameTable
from iarlib.pointertype import PointerType
section_type[PointerType.ID()] = PointerType
from iarlib.type import Type
section_type[Type.ID()] = Type

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
    else:
        pprint(sections)
        print(f"Unknown section ID: {section_id:02X}")
        exit(1)

pprint(sections)