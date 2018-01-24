import memory
import struct
import sys


OFFSETS = {'CGCamera::m_fov': 64,
           's_currentWorldFrame': 11672552,
           'CGWorldFrame::m_camera': 26060
           }
 
class WowCamera(object):

    def __init__(self, mem):
        self.mem = mem
    
    def update_camera_address(self):
        pWorldFrame = self.mem.read('I', OFFSETS['s_currentWorldFrame'])
        if not pWorldFrame:
            print("static worldFrame null!")
            return

        pCamera = self.mem.read('I', pWorldFrame + OFFSETS['CGWorldFrame::m_camera'])
        if not pCamera:
            print("worldFrame m_camera null!")
            return

        self.pcam = pCamera

    def get_fov(self):
        self.update_camera_address()
        return self.mem.read('f', self.pcam + OFFSETS['CGCamera::m_fov'])

    def set_fov(self, val):
        self.update_camera_address()
        self.mem.write('f', self.pcam + OFFSETS['CGCamera::m_fov'], val)


def main():
    m = memory.Memory(int(sys.argv[1]))
    cam = WowCamera(m)

    while True:
        print("current fov is ", cam.get_fov(), " change?")
        cam.set_fov(float(input()))

if __name__ == '__main__':
    main()
