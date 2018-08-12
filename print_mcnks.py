#! /usr/bin/env python3

from wow import adt, simple_file
from sys import argv


fn = argv[1]
a = adt.AdtFile()
a.load(simple_file.load(fn))

asdict = vars(a)

for attr in asdict:
    if attr not in ('chunks', 'doodad_names'):
        print(attr, asdict[attr])

for mcnk in a.chunks:
    print(' '.join([str(n) for n in mcnk.chunknames]))

