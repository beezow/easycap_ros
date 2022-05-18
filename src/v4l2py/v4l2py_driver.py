from device import Device

class EasyCap:
    def __init__(self, cam_number):
        self.cam = Device.from_id(cam_number)

    def __del__(self):
        self.cam.close()

    def stream(self):



