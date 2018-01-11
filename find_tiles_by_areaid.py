#! /usr/bin/env python3

import sys
import os.path

from collections import namedtuple

from wow import adt, dbc
from wow.wdt import Wdt
from wow.simple_file import load

GAME_ROOT = "/Users/jrsa/wow/wowassets/wotlk"
MAPS_ROOT = "World/Maps/"
DBC_ROOT = "dbc/"

# harder mode: resolve dual results for root area, i.e., for instanced dungeons
# harder mode 2: resolve area's which are only present in WMO's

def usage():
    print("usage: {} <area name>".format(sys.argv[0]))


def get_areas_for_name(name):
    areatable = dbc.DbcFile(dbc.format_import.FormatImport().get_format('AreaTable'))
    areatable.load(load(os.path.join(GAME_ROOT, DBC_ROOT, 'AreaTable.dbc')))

    # there can be multiple id's if the specified area is the parent area of
    # another area
    ids = []

    parent_id = 0
    map_id = None
    names = dict()

    # find parent (exact match for name argument)
    for r in areatable.records:
        if r[11] == name:
            map_id = r[1]
            parent_id = r[0]
            ids.append(parent_id)
            names[parent_id] = r[11]
            break

    # find children
    if parent_id != 0:
        for r in areatable.records:
            if r[2] == parent_id:
                ids.append(r[0])
                names[r[0]] = r[11]

    return ids, names, map_id


def get_map_dir_for_id(mapid):
    mapdb = dbc.DbcFile(dbc.format_import.FormatImport().get_format("Map"))
    mapdb.load(load(os.path.join(GAME_ROOT, DBC_ROOT, 'Map.dbc')))

    for r in mapdb.records:
        if r[0] == mapid:
            return r[1]

    print("map not found for id ", mapid)
    return


def main():
    TileEntry = namedtuple('TileEntry', ['x', 'y', 'areaid'])

    matches = []

    try:
        area_to_find = sys.argv[1]
    except IndexError as e:
        usage()
        sys.exit(-1)

    area_ids_to_find, names_by_id, map_id = get_areas_for_name(area_to_find)
    if map_id is None:
        return

    map_name = get_map_dir_for_id(map_id)

    print("{} is on the map: {}".format(area_to_find, map_name))

    wdt_filename = "{name}/{name}.wdt".format(name=map_name)
    wdt = Wdt()
    wdt.read(load(os.path.join(GAME_ROOT, MAPS_ROOT, wdt_filename)))

    if len(wdt.extant_tiles):
        for i, j in wdt.extant_tiles:
            tile_fn = "{name}/{name}_{x}_{y}.adt".format(name=map_name, x=i, y=j)
            tile_fullpath = os.path.join(GAME_ROOT, MAPS_ROOT, tile_fn)
            a = adt.AdtFile()
            a.load(load(tile_fullpath))
            for c in a.chunks:
                if c.areaId in area_ids_to_find and TileEntry(i, j, c.areaId) not in matches:
                    matches.append(TileEntry(i, j, c.areaId))

        for entry in matches:
            tile_fn = "{name}_{x}_{y}.adt".format(name=map_name, x=entry.x, y=entry.y)
            print("{} contains {}".format(tile_fn, names_by_id[entry.areaid]))

    elif len(wdt.object_filename):
        print("no map tiles found, only global wmo: ", wdt.object_filename)

    else:
        print("invalid wdt file (what the fuck)")

if __name__ == '__main__':
    main()
