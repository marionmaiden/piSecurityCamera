#!/usr/bin/env python

from io       import BytesIO
from picamera import PiCamera
from PIL      import Image, ImageChops
from time     import sleep
from datetime import datetime
import math

threshold = 400

def isDiff(a, b):
    diff = ImageChops.difference(a, b)
    diffl = list(diff.getdata())

    res = math.fsum(max(diffl, key = lambda i : math.fsum(i)))

    print("Comparacao: {}".format(res))

    return res > threshold

#    for i in diffl:
#        print (i)
#        if math.fsum(i) > threshold:
#            print("-> Encontrou diferenca!!")
#            return True
#    return False



def main():
    baseImgName = "base.jpg"
    capturedImgName = "cap{}.jpg"

    stream = BytesIO()
    camera = PiCamera()
    camera.resolution = (1280,720)

    print("-> Capturando a imagem base")
    sleep(2)
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    baseImg = Image.open(stream)

    baseImg.save(baseImgName, "JPEG")


    while 1:
        stream = BytesIO()
        print("-> Capturando a imagem atual")
        sleep(2)
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        currImg = Image.open(stream)

        if isDiff(baseImg, currImg):
            print("-> Salvando a imagem com diferenca")
            currImg.save(capturedImgName.format(datetime.now()),"JPEG")
            baseImg = currImg



if __name__ == "__main__": main()
