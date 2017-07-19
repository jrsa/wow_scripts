#! /usr/bin/env python3

from wow import adt, simple_file
from sys import argv


fn = argv[1]
a = adt.AdtFile()
a.load(simple_file.load(fn))
# print(a)

