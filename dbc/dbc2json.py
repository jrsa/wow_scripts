#! /usr/bin/env python3

"""
converts a DBC file to JSON format, using python 3s json module
"""

import sys
import os.path
import json

import wow.simple_file as sfile
from wow.dbc import DbcFile
from wow.dbc.format_import import FormatImport

try:
	fn = sys.argv[1]
	map_fn = sys.argv[2]
except IndexError as e:
	print("usage: {} <dbc filename> <xml definition filename>".format(sys.argv[0]))
	sys.exit(1)

f = sfile.load(fn)

rec_format = FormatImport(map_fn).get_format(os.path.basename(fn))
inst = DbcFile(rec_format)
inst.load(f)

path = os.path.basename(fn) + ".json"
print("saving to {}".format(path))

with open(path, "w") as f:
    json.dump(inst.records, f)