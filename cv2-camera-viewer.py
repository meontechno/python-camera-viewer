import time

import cv2


WIDTH, HEIGHT = 640, 480
FRAME_RATE = 30


class Camera:
    def __init__(self, device="/dev/video0", size=(640, 480)):
        self._device_pth = device
        self._size = size
        self._open = False

    def start(self):
        if self._open:
            return

        self._cam = cv2.VideoCapture(self._device_pth)

        if not self._cam.isOpened():
            raise ValueError("Could not open camera.")

        self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, self._size[0])
        self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self._size[1])

        w = self._cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self._size = (int(w), int(h))
        self._frame_time = 1 / self._cam.get(cv2.CAP_PROP_FPS)
        self._last_frame_time = 0

        self._open = True

    def stop(self):
        if self._open:
            self._cam.release()
            self._cam = None
            self._open = False

    def _check_open(self):
        if not self._open:
            raise ValueError("Could not open camera")

    def get_image(self):
        self._check_open()

        self._last_frame_time = time.time()

        ret, image = self._cam.read()
        if not ret:
            raise ValueError("Could not read frames")

        return image

    def view(self):
        self._check_open()

        while self._open:
            cv2.imshow("{self._device_pth}", self.get_image())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return


if __name__ == "__main__":
    cam = Camera()
    cam.start()
    print(cam.get_image())
    cam.view()
    cam.stop()
