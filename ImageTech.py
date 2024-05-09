import cv2



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