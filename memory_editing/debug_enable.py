from mem import Memory
import sys

from offsets import OFFSETS


def main():
    m = Memory(int(sys.argv[1]))

    en = m.read('I', OFFSETS[12340]['debug_enable'])

    print("current debug enable value", en)

    m.write('I', OFFSETS[12340]['debug_enable'], 1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
