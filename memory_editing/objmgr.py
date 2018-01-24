import memory
import sys


def visible(mem):
    mgr = mem.read('I', 0x99066c)
    obj = mem.read('I', mgr + 0xb4)
    offs = mem.read('I', mgr + 0xac)

    while(not obj & 1 and obj is not 0):
        yield(obj)
        obj = mem.read('I', obj + offs + 4)

def unit_name(mem, unit_addr):
    pstats = mem.read('I', unit_addr + 0xb24)


def main():
    m = memory.Memory(int(sys.argv[1])) # specify pid on commandline

    for o in visible(m): 
        data = m.read('I', o + 0x4)
        guid = m.read('L', o + 0x28)
        type = m.read('I', data + 0x8)

        if type & 8 is not 0:
            pstats = m.read('I', o + 0xb24) # read stats pointer out of m_stats field on CGUnit_C
            if pstats is not 0: # players will have the UNIT bit set but will not have the m_stats field
                ppname = m.read('I', pstats)
                pname = m.read('I', ppname)
                namebytes = m.read_n(ppname, 0x20)
                name = namebytes[0:namebytes.index(0)].decode('ascii')

            if not name:
                name = 'unknown being'
            print("{}: {}".format(name, format(guid, '#02x')))

if __name__ == '__main__':
    main()