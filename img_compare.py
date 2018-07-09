from os import system
import numpy as np
import cv2

"""-------------GLOBAL VARIABLES------------"""

HISTOGRAM_DIFF_THRESHOLD = 1
FIRST_CAMERA_ID = 0
SECOND_CAMERA_ID = 1

global_imageCounter = 0



"""-------------FUNCTIONS------------"""

def takePhoto(imagePath, cameraId):
	comando = "fswebcam -d /dev/video" + str(cameraId) + " " + imagePath
	system(comando)

def getImagePath(imageId):
	return "img-" + str(imageId) + ".jpeg"

def getImageHist(imagePath):
	image = cv2.imread(imagePath)
	hist = cv2.calcHist(image, [0], None, [8],[0, 256])
	hist = cv2.normalize(hist).flatten()
	print(hist)
	return hist

def compareImages(firstImagePath, secondImagePath):
	firstHist  = getImageHist(firstImagePath)
	secondHist = getImageHist(secondImagePath)
	diff = cv2.compareHist(firstHist, secondHist, method=cv2.CV_COMP_CHISQR)
	print(diff)
	if diff >= HISTOGRAM_DIFF_THRESHOLD:
		return True
	else:
		return False



"""-------------TEST------------"""

def test():
    imgPath1 = getImagePath(global_imageCounter)
    takePhoto(imgPath1, FISRT_CAMERA_ID)
    global_imageCounter += 1
    imgPath2 = getImagePath(global_imageCounter
    takePhoto(imgPath2, SECOND_CAMERA_ID)
    global_imageCounter += 1
    imgPath3 = getImagePath(global_imageCounter)
    takePhoto(imgPath3, FISRT_CAMERA_ID)
    global_imageCounter += 1
    imgPath4 = getImagePath(global_imageCounter
    takePhoto(imgPath4, SECOND_CAMERA_ID)
    global_imageCounter += 1

    comp1 = compareImages(imagePath1, imagePath3)
    comp2 = compareImages(imagePath2, imagePath4)
    print(comp1)
    print(comp2)

	




test()


	
