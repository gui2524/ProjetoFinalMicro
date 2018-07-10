from os import system
import numpy as np
import cv2
import log
import os

"""-------------GLOBAL VARIABLES------------"""

global_diretorio_atual = os.path.dirname(os.path.abspath(__file__))
HISTOGRAM_DIFF_THRESHOLD = 1
FIRST_CAMERA_ID = 0
SECOND_CAMERA_ID = 1
THIRD_CAMERA_ID = 2

global_imageCounter = 0



"""-------------FUNCTIONS------------"""

def takePhoto(cameraId):
    global global_imageCounter
    imagePath = getImagePath(global_imageCounter)
    global_imageCounter += 1
    comando = "fswebcam -d /dev/video" + str(cameraId) + " " + imagePath
    log.log(comando)
    system(comando)

    try:
        open(imagePath, "rb")
    except:
        system(comando)
    
    return imagePath

def getImagePath(imageId):
    return global_diretorio_atual + "/photos/img-" + str(imageId) + ".jpeg"

def getImageHist(imagePath):
    image = cv2.imread(imagePath)
    hist = cv2.calcHist(image, [0], None, [8],[0, 256])
    hist = cv2.normalize(hist).flatten()
    return hist

def compareImages(firstImagePath, secondImagePath):
    firstHist  = getImageHist(firstImagePath)
    secondHist = getImageHist(secondImagePath)
    diff = cv2.compareHist(firstHist, secondHist, method=cv2.cv.CV_COMP_CHISQR)
    log.log(str(diff))
    if diff >= HISTOGRAM_DIFF_THRESHOLD:
        return True
    else:
        return False



"""-------------TEST------------"""

##path1 = getImagePath(0)
##takePhoto(path1, FIRST_CAMERA_ID)
##path = getImagePath(1)
##takePhoto(path, FIRST_CAMERA_ID)
##compareImages(path1, path)
