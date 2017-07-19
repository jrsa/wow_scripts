#! /usr/bin/env python3


from wow import chunks, simple_file
import sys

try:
    fn = sys.argv[1]
except IndexError as e:
    print("specify a filename as first argument, pls")

for c, sz, d in chunks.chunks(simple_file.load(fn)):
    print(c[::-1], sz) # prints chunk ID backwards