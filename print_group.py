"""
prints all the chunk names and sizes inside a wmo group file
(contents of the MOGP chunk)
"""

from wow import chunks, simple_file
import struct
import sys

try:
    fn = sys.argv[1]
except IndexError as e:
    print("specify a filename as first argument, pls")

for c, sz, d in chunks.chunks(simple_file.load(fn)):
    print(c[::-1], sz) # prints chunk ID backwards
    if c == b'PGOM':
        print('\tgroup header:')
        hdr = struct.unpack(17 * 'I', d[:68])
        print(hdr)

        print('\tgroup subchunks:')
        for subchunkid, subchunksize, subchunkdata in chunks.chunks(d[68:]):
            print('\t', subchunkid[::-1], subchunksize)