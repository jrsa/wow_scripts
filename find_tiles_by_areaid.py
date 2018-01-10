#! /usr/bin/env python3

import sys
import os.path

from wow import adt, dbc
from wow.wdt import Wdt
from wow.simple_file import load

GAME_ROOT = "/Users/jrsa/wow/wowassets/wotlk"
MAPS_ROOT = "World/Maps/"
DBC_ROOT = "dbc/"


def usage():
    print("usage: {} <map name> <area name>".format(sys.argv[0]))


def get_areas_for_name(name):
    areatable = dbc.DbcFile(dbc.format_import.FormatImport().get_format('AreaTable'))
    areatable.load(load(os.path.join(GAME_ROOT, DBC_ROOT, 'AreaTable.dbc')))

    # there can be multiple id's if the specified area is the parent area of
    # another area
    ids = []

    parent_id = 0
    names = dict()

    # find parent (exact match for name argument)
    for r in areatable.records:
        if r[11] == name:
            parent_id = r[0]
            ids.append(parent_id)
            names[parent_id] = r[11]

    # find children
    if parent_id != 0:
        for r in areatable.records:
            if r[2] == parent_id:
                ids.append(r[0])
                names[r[0]] = r[11]

    return ids, names


def main():
    matches = []

    wdt_filename = "{name}/{name}.wdt".format(name=sys.argv[1])
    wdt = Wdt()
    wdt.read(load(os.path.join(GAME_ROOT, MAPS_ROOT, wdt_filename)))

    try:
        area_to_find = sys.argv[2]
    except IndexError as e:
        usage()
        sys.exit(-1)

    area_ids_to_find, names_by_id = get_areas_for_name(area_to_find)

    if len(wdt.extant_tiles):
        for i, j in wdt.extant_tiles:
            tile_fn = "{name}/{name}_{x}_{y}.adt".format(name=sys.argv[1], x=i, y=j)
            tile_fullpath = os.path.join(GAME_ROOT, MAPS_ROOT, tile_fn)
            if os.path.exists(tile_fullpath):
                a = adt.AdtFile()
                a.load(load(tile_fullpath))
                for c in a.chunks:
                    if c.areaId in area_ids_to_find:
                        if (((i, j), c.areaId)) not in matches:
                            matches.append(((i, j), c.areaId))
            else:
                print("ERROR: {} doesnt exist".format(tile_fn))

        for tile in matches:
            print("tile {} contains {}".format(tile[0], names_by_id[tile[1]]))

    elif len(wdt.object_filename):
        print("no map tiles found, only global wmo: {}", wdt.object_filename)

    else:
        print("invalid wdt file (what the fuck)")

if __name__ == '__main__':
    main()
