#! /usr/bin/env python3

import sys
import os.path

from wow.wdt import Wdt
from wow.simple_file import load

mapname = sys.argv[1]

data_root = "/Users/jrsa/wow/wowassets/wotlk/"
maps_root = os.path.join(data_root, 'World/Maps/')
wdt_filename = f"{mapname}/{mapname}.wdt"

wdt = Wdt()
wdt.read(load(os.path.join(maps_root, wdt_filename)))

print("read wdt file, version=", wdt.version)

if len(wdt.extant_tiles):
    print(f"found {len(wdt.extant_tiles)} tiles")

    for i, j in wdt.extant_tiles:
        tile_fn = os.path.join(maps_root, f"{mapname}/{mapname}_{i}_{j}.adt")
        if os.path.exists(tile_fn):
            print("adt found for", i, j)
        else:
            print("error: no adt file found for", i, j)

elif len(wdt.object_filename):
    print("found object file", wdt.object_filename)

else:
    print("didnt find tiles or wmo, read a bad file without throwing an error!")
