#! /usr/bin/env python3

import sys
from os.path import exists, join, sep

from wow.wdt import Wdt
from wow.simple_file import load

mapname = sys.argv[1]

data_root = "/Users/jrsa/wow/wowassets/wotlk/"
maps_root = join(data_root, 'World/Maps/')
wdt_filename = f"{mapname}/{mapname}.wdt"

wdt = Wdt()
wdt.read(load(join(maps_root, wdt_filename)))

print("read wdt file, version=", wdt.version)

if len(wdt.extant_tiles):
    print(f"found {len(wdt.extant_tiles)} tiles")

    for i, j in wdt.extant_tiles:
        tile_fn = join(maps_root, f"{mapname}/{mapname}_{i}_{j}.adt")
        if exists(tile_fn):
            print("adt found for", i, j)
        else:
            print("error: no adt file found for", i, j)

elif len(wdt.object_filename):
    wmo_path = join(data_root, sep.join(wdt.object_filename.decode('utf-8').split('\\')))
    if exists(wmo_path):
        print("found object file on disk: ", wmo_path)

else:
    print("didnt find tiles or wmo, read a bad file without throwing an error!")
