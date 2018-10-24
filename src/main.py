import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from process import get_line
import cv2
import drive
import utils

# Camera initialization

camera = PiCamera()
camera.resolution = (utils.width, utils.height)      # Camera resolution
camera.framerate = utils.fps               # FPS
rawCapture = PiRGBArray(camera, size=(utils.width, utils.height))

# Motor initialization

drive.initialize()

time.sleep(0.5)

print("Start driving.")

try:
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        image = frame.array

        # Detect line from image / get angle & image
        line = get_line(image)

        angle = line.get('angle', None)
        drive.driveAngle(angle)

        cv2.imshow('preview', line.get('image', None))

        rawCapture.truncate(0)

        # Press Q to quit
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
except:
    pass

drive.driveAngle(None)
drive.clean()
print("Stop driving.")
quit()
