import cv2
import numpy as np


def edgeDetection(img): # Canny
    return cv2.Canny(img,100,200)
    

def colorInversion(img):
    return cv2.bitwise_not(img)

def convertToGray(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def applyBlurring(img):
    return cv2.blur(img,(5,5))

def applyGaussianBlur(img):
    return cv2.GaussianBlur(img,(5,5),3)

def applyErosion(img):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(img)


def applyDilation(img):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(img)

def resizeImgToHalf(img):
    return cv2.resize(img,fx=0.5,fy=0.5)

def increaseBrightness(img):
    brightness = 15
    contrast = 1.5
    image2 = cv2.addWeighted(img, contrast, np.zeros(img.shape, img.dtype), 0, brightness) 
def removeNoise(img):
    return cv2.medianBlur(img,11)




def ApplyTechnique(img,method):

    if method == "edgeDetection":
        return edgeDetection(img.copy())

    elif method == "colorInversion":
        return colorInversion(img.copy())

    elif method == "convertToGray":
        return convertToGray(img.copy())
    
    elif method == "applyBlurring":

        return applyBlurring(img.copy())

    elif method == "applyGaussianBlur":
        return applyGaussianBlur(img.copy())

    else:
        print(f"Technique '{method}' not found.")

img = cv2.imread('')

result = ApplyTechnique(img,'')

cv2.imshow('Original Image',img)

cv2.imshow('Output Image',result)

cv2.waitKey()