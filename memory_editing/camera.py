import mem
import struct
import sys

from offsets import OFFSETS

BUILD_NUMBER = 5875
OFFSETS = OFFSETS[BUILD_NUMBER]
 
class WowCamera(object):

    def __init__(self, mem):
        self.mem = mem
    
    def update_camera_address(self):
        pWorldFrame = self.mem.read('I', OFFSETS['s_currentWorldFrame'])
        if not pWorldFrame:
            raise RuntimeError("static worldFrame null!")

        pCamera = self.mem.read('I', pWorldFrame + OFFSETS['CGWorldFrame::m_camera'])
        if not pCamera:
            raise RuntimeError("worldFrame m_camera null!")

        self.pcam = pCamera

    def get_fov(self):
        self.update_camera_address()
        return self.mem.read('f', self.pcam + OFFSETS['CGCamera::m_fov'])

    def set_fov(self, val):
        self.update_camera_address()
        self.mem.write('f', self.pcam + OFFSETS['CGCamera::m_fov'], val)


def main():
    m = mem.Memory(int(sys.argv[1]))
    cam = WowCamera(m)

    # cam.update_camera_address()

    while True:
        print("current fov is ", cam.get_fov(), " change?")
        cam.set_fov(float(input()))

if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        print(e)
    except (EOFError, KeyboardInterrupt) as e:
        print("goodbye")