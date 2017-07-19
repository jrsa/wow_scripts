#! /usr/bin/env python3

import sys
import os.path
import json

from wow.dbc import DbcFile
from wow.dbc.format_import import FormatImport
import wow.simple_file as sf

fn = sys.argv[1]

# bring in json
with open(fn, "r") as f:
    json_data = f.read()

records = json.loads(json_data)

# get dbc format specifier
dbc_name = os.path.splitext(os.path.basename(fn))[0]

# create a new dbc with the imported records
fi = FormatImport().get_format(dbc_name)
new_dbc = DbcFile(fi)
new_dbc.records = records

sf.save("exported_" + dbc_name, new_dbc.save())
