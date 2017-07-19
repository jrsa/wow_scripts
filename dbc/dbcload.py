#! /usr/bin/env python3

# just prints out the records inside a dbc file

import sys
import os.path
from wow import dbc, simple_file

fn = sys.argv[1]

inst = dbc.DbcFile(dbc.format_import.FormatImport().get_format(os.path.basename(fn)))
inst.load(simple_file.load(fn))

for r in inst.records:
    print(r)
