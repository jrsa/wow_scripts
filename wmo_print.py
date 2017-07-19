#! /usr/bin/env python3

import sys
from wow import wmo, simple_file


fn = sys.argv[1]


inst = wmo.root.Root()
inst.load( simple_file.load( fn ) )

