from mem import Memory
import sys


ENABLES = 0xB60E90


def main():
    m = Memory(int(sys.argv[1]))

    while True:
        enables = m.read('I', ENABLES)

        bit = 0
        try:
            bit = int(input("toggle flag: "))
        except ValueError as e:
            print("please enter an integer")
        else:

            flag = 1 << bit

            if (enables & flag) is not 0:
                enables = enables & (~flag)
            else:
                enables = enables | flag

            m.write('I', ENABLES, enables)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)