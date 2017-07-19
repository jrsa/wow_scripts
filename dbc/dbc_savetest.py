#! /usr/bin/env python3

import sys
import os.path
import json

import wow.simple_file as sfile
from wow.dbc import DbcFile, format_import

fn = sys.argv[1]

f = sfile.load(fn)

rec_format = format_import.FormatImport().get_format(os.path.basename(fn))
inst = DbcFile(rec_format)
inst.load(f)

# sfile.save(os.path.basename(fn) + ".testsave", inst.save())
sfile.save(os.path.basename(fn) + ".json", json.dumps(inst.records))
