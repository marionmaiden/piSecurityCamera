#!/usr/bin/python3

from datetime import datetime
from PIL      import Image, ImageChops
from PIL      import ImageFilter

from .emailsender import EmailSender
from .camera import Camera

import math
import statistics

class SecurityCamera(object):

    # constants
    storeThreshold = 15
    emailThreshold = 50
    emailPropertiesFile = "../resources/email.properties"
    prefix = "./img/"
    baseImgName = "base.jpg"
    capturedImgName = "cap{}.jpg"

    def __init__(self):
        self.camera = Camera()
        # self.email = EmailSend(emailPropertiesFile)

    """
    	Calculate if two images (a and b) are different or not
    	- apply gaussian blur to both images and resize it to a 8x6 matrix
    	- calculate the image difference by subtracting the pixel values from aij and bij
    	- calculate the pixel difference mean
    	- if the mean is bigger than the threshold, both images are considered different
    """
    def isDiff(self, a, b):
        diff = ImageChops.difference(a.filter(ImageFilter.GaussianBlur(2)).resize((8,8), Image.LANCZOS), b.filter(ImageFilter.GaussianBlur(2)).resize((8,8), Image.LANCZOS))
        diffl = list(diff.getdata())

        # Converting a list of tuples to list
        res = statistics.mean(map(math.fsum, diffl))

        print("Image diff value: {}".format(res))

        return res


    """
    """
    def run(self):

        print("-> Base image")
        baseImg = self.camera.readImg()

        self.camera.saveImg(self.prefix, baseImg, self.baseImgName)

        while 1:
            print("-> Current image")
            currImg = self.camera.readImg()

            difference = self.isDiff(baseImg, currImg)

            if  difference > self.storeThreshold:
                print("-> Saving the image with difference")
                filename = self.capturedImgName.format(datetime.now())

                self.camera.saveImg(self.prefix, currImg, filename)
                baseImg = currImg

                if difference > self.emailThreshold:
                    print("-> High threshold - sending e-mail")
                    self.email.sendEmail(filename)
