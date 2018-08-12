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
from optparse import OptionParser


from wow.simple_file import load, save
from wow.dbc import DbcFile, FormatError
from wow.dbc.format_import import FormatImport


def test(opts, formatter):
    fullpath = join(opts.in_dir, opts.filename + ".dbc")
    f = load(fullpath)

    inst = DbcFile(formatter.get_format(opts.filename))
    inst.load(f)

    output_path = join(opts.out_dir, opts.filename + ".dbc")
    save(output_path, inst.save())


def main(opts, formatter):
    errors = []

    for entry in formatter.root.getchildren():
        name = entry.tag
        opts.filename = name
        try:
            test(opts, formatter)
        except Exception as e:
            errors.append((name, e))

    print("{} total errors: ".format(len(errors)))

    notfounderrors = [e for e in errors if type(e[1]) == FileNotFoundError]
    print("{} not found".format(len(notfounderrors)))
    for e in notfounderrors:
        print("{}: {}".format(e[0], e[1].args[0]))

    typeerrors = [e for e in errors if type(e[1]) == TypeError]
    print("{} type errors".format(len(typeerrors)))
    for e in typeerrors:
        print("{}: {}".format(e[0], e[1].args[0]))

    formaterrors = [e for e in errors if type(e[1]) == FormatError]
    print("{} format errors".format(len(formaterrors)))
    for e in formaterrors:
        print("{}: {}".format(e[0], e[1].args[0]))

if __name__ == '__main__':

    parser = OptionParser()
    
    parser.add_option('-n', '--name', dest='filename', help='name of a single dbc file (without extension) to process')
    parser.add_option('-d', '--def', dest='mapfn', help='path to the definition file')
    parser.add_option('-i', '--input', dest='in_dir', default='.', help='directory containing dbc files to process')
    parser.add_option('-o', '--output', dest='out_dir', default='./output/', help='directory in which processed files will be saved')
    
    (options, args) = parser.parse_args()

    if options.mapfn:
        formats = FormatImport(options.mapfn)
    else:
        formats = FormatImport()

    if options.filename is None:
        main(options, formats)
    else:
        test(options, formats)
