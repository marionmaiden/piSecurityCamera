#!/usr/bin/env python

from io       import BytesIO
from picamera import PiCamera
from PIL      import Image
from time     import sleep
import os

class Camera:


    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1296,972)

    """
    """
    def readImg(self):
        stream = BytesIO()
        sleep(2)
        self.camera.capture(stream, format="jpeg")
        stream.seek(0)
        return Image.open(stream)

    """
    """
    def saveImg(self, prefix ,img, name):
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        img.save(prefix + name, "JPEG")
