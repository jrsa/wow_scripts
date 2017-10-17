#! /usr/bin/env python3

"""
this script will attempt verify correct loading and saving of 
all DBC files covered by the FormatImport class. if one dbc filename
is specified it will just try that one.

specify the path to all the dbc files below
"""

import logging

from os.path import join, basename
from sys import argv, exit

from wow.simple_file import load, save
from wow.dbc import DbcFile, FormatError
from wow.dbc.format_import import FormatImport

dbc_folder = None
formats = None


def test(name):
    fullpath = join(dbc_folder, name + ".dbc")
    f = load(fullpath)

    inst = DbcFile(formats.get_format(name))
    inst.load(f)

    output_path = join(dbc_folder, "testoutput", name + ".dbc")
    save(output_path, inst.save())


def main(mapfn):
    global formats
    errors = []
    formats = FormatImport(mapfn)
    for entry in formats.root.getchildren():
        name = entry.attrib['Name']
        try:
            test(name)
        except Exception as e:
            errors.append((name, e))

    print("{} total errors: ".format(len(errors)))
    
    notfounderrors = [e for e in errors if type(e[1]) == FileNotFoundError]
    print("{} not found".format(len(notfounderrors)))
    # print(notfounderrors[0])

    typeerrors = [e for e in errors if type(e[1]) == TypeError]
    print("{} type errors".format(len(typeerrors)))
    for e in typeerrors: print("{}: {}".format(e[0], e[1].args[0]))

    formaterrors = [e for e in errors if type(e[1]) == FormatError]
    print("{} format errors".format(len(formaterrors)))
    for e in formaterrors: print("{}: {}".format(e[0], e[1].args[0]))

if __name__ == '__main__':
    tryall = None

    dbc_folder = "."
    # print(dbc_folder)
    # exit(1)

    try:
        mapfn = argv[1]
    except IndexError as e:
        print("usage: {} <xml definition> [dbc filename]".format(argv[0]))
        exit(1)

    try:
        name = argv[2]
        tryall = False
    except IndexError:
        tryall = True

    if tryall:
        main(mapfn)
    else:
        test(name)
