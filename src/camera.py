#!/usr/bin/env python

from io       import BytesIO
from picamera import PiCamera
from PIL      import Image, ImageChops
from PIL      import ImageFilter
from time     import sleep
from datetime import datetime
import math
import statistics
import os
from emailsender import EmailSender

# constants
threshold = 10
prefix = "../img/"
baseImgName = prefix + "base.jpg"
capturedImgName = prefix + "cap{}.jpg"

"""
	Calculate if two images (a and b) are different or not
	- apply gaussian blur to both images and resize it to a 8x8 matrix
	- calculate the image difference by subtracting the pixel values from aij and bij
	- calculate the pixel difference mean
	- if the mean is bigger than the threshold, both images are considered different
"""
def isDiff(a, b):
    diff = ImageChops.difference(a.filter(ImageFilter.GaussianBlur(2)).resize((8,8), Image.LANCZOS), b.filter(ImageFilter.GaussianBlur(2)).resize((8,8), Image.LANCZOS))
    diffl = list(diff.getdata())

    # Converting a list of tuples to list
    res = statistics.mean(map(math.fsum, diffl))

    print("Image diff value: {}".format(res))

    return res > threshold

"""
"""
def readImg(camera):
    stream = BytesIO()
    sleep(2)
    camera.capture(stream, format="jpeg")
    stream.seek(0)
    return Image.open(stream)

"""
"""
def saveImg(img, name):
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    img.save(name, "JPEG")

"""
"""
def main():

    email = EmailSend("../resources/email.properties")

    camera = PiCamera()
    camera.resolution = (1280,720)

    print("-> Base image")
    baseImg = readImg(camera)

    saveImg(baseImg, baseImgName)

    while 1:
        print("-> Current image")
        currImg = readImg(camera)

        if isDiff(baseImg, currImg):
            print("-> Saving the image with difference")
            filename = capturedImgName.format(datetime.now())
            saveImg(currImg, filename)
            email.sendEmail(filename)
            baseImg = currImg



if __name__ == "__main__": main()
