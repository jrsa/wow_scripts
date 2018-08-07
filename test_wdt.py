#! /usr/bin/env python3

import sys
import os.path

from wow.wdt import Wdt
from wow.simple_file import load

maps_root = "/Users/jrsa/wow/12340/Data/World/Maps/"
wdt_filename = "{name}/{name}.wdt".format(name=sys.argv[1])

wdt = Wdt()
wdt.read(load(maps_root + wdt_filename))

print("read wdt file, version=", wdt.version)

if len(wdt.extant_tiles):
    print("found {n} tiles".format(n=len(wdt.extant_tiles)))

    for i, j in wdt.extant_tiles:
        tile_fn = maps_root + "{name}/{name}_{x}_{y}.adt".format(name=sys.argv[1], x=i, y=j)
        if os.path.exists(tile_fn):
            print("adt found for", i, j)
        else:
            print("error: no adt file found for", i, j)

elif len(wdt.object_filename):
    print("found object file", wdt.object_filename)

else:
    print("didnt find tiles or wmo, read a bad file without throwing an error!")
