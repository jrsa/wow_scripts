import mem
import sys


from offsets import OFFSETS

BUILD_NUMBER = 5875
OFFSETS = OFFSETS[BUILD_NUMBER]

def visible(mem):
    mgr = mem.read('I', OFFSETS['s_curMgr'])
    obj = mem.read('I', mgr + 0xb4)
    offs = mem.read('I', mgr + 0xac)

    while(not obj & 1 and obj is not 0):
        yield(obj)
        obj = mem.read('I', obj + offs + 4)

def unit_name(mem, unit_addr):
    pstats = mem.read('I', unit_addr + 0xb24) # read stats pointer out of m_stats field on CGUnit_C
    if pstats is not 0: # players will have the UNIT bit set but will not have the m_stats field
        ppname = mem.read('I', pstats)
        pname = mem.read('I', ppname)
        namebytes = mem.read_n(ppname, 0x30)
        return namebytes[0:namebytes.index(0)].decode('ascii')
    else:
        return "unknown being"

def gameobject_name(mem, gobject_addr):
    pstats = mem.read('I', gobject_addr + 524)
    if pstats is not 0:
        pname = mem.read('I', pstats + 0x8)
        if pname is not 0:
            namebytes = mem.read_n(pname, 0x30)
            return(namebytes[0:namebytes.index(0)].decode('ascii'))

def main():
    m = mem.Memory(int(sys.argv[1])) # specify pid on commandline

    for o in visible(m): 
        data = m.read('I', o + 0x4)
        guid = m.read('L', o + 0x28)
        type = m.read('I', data + 0x8)

        name = None

        if type & 8 is not 0:
            name = unit_name(m, o)
            print("[UNIT]:\t{}:\t{}".format(format(guid, '#02x'), name))

        if type & 32 is not 0:
            name = gameobject_name(m, o)
            print("[GOBJ]:\t{}:\t{}".format(format(guid, '#02x'), name))


if __name__ == '__main__':
    main()