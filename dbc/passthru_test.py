#! /usr/bin/env python3

"""
this script will attempt verify correct loading and saving of 
all DBC files covered by the FormatImport class. if one dbc filename
is specified it will just try that one.

specify the path to all the dbc files below
"""

import logging

from os.path import join
from sys import argv

from wow.simple_file import load, save
from wow.dbc import DbcFile, FormatError
from wow.dbc.format_import import FormatImport

DBC_DIRECTORY = "/Users/jrsa/wow/wowassets/wotlk/dbc"

formats = FormatImport()


def test(name):
    fullpath = join(DBC_DIRECTORY, name + ".dbc")
    f = load(fullpath)

    inst = DbcFile(formats.get_format(name))
    inst.load(f)

    output_path = join(DBC_DIRECTORY, "testoutput", name + ".dbc")
    save(output_path, inst.save())


def main():
    errors = []
    for entry in formats.root.getchildren():
        name = entry.attrib['Name']
        try:
            test(name)
        except Exception as e:
            errors.append((name, e))

    print("{} total errors: ".format(len(errors)))
    
    notfounderrors = [e for e in errors if type(e[1]) == FileNotFoundError]
    print("{} not found".format(len(notfounderrors)))

    typeerrors = [e for e in errors if type(e[1]) == TypeError]
    print("{} type errors".format(len(typeerrors)))
    for e in typeerrors: print("{}: {}".format(e[0], e[1].args[0]))

    formaterrors = [e for e in errors if type(e[1]) == FormatError]
    print("{} format errors".format(len(formaterrors)))
    for e in formaterrors: print("{}: {}".format(e[0], e[1].args[0]))

if __name__ == '__main__':
    tryall = None
    try:
        name = argv[1]
        tryall = False
    except IndexError:
        tryall = True

    if tryall:
        main()
    else:
        test(name)
