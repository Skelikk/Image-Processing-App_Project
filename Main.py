import  cv2
import numpy as np
from skimage.feature.texture import graycomatrix, graycoprops
from skimage.feature import local_binary_pattern

def rgb_histogram(image, bins=256):
    b = image.copy()
    g = image.copy()
    r = image.copy()
    b[:,:,1] = 0
    b[:,:,2] = 0
    g[:,:,0] = 0
    g[:,:,2] = 0
    r[:,:,0] = 0
    r[:,:,1] = 0
    return [b,g,r]

def GaussianBlurVariables(direction=1, sigmaX=0):
    if direction%2 != 0:
        direction_xy = (direction, direction)
        return (direction_xy, sigmaX)
    else:
        Exception("Direction must be an odd number")

def edgeParameters(x=0,y=0):
    return [x,y]

image_path = r'C:/Users/Admaj/Downloads/singals/Signal_Project/shit.jpg'
image_color = cv2.imread(image_path)
if image_color is None:
    print("Could not open or find the image")
    exit(0)
image_grey = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
cv2.imshow('R', rgb_histogram(image_color)[2])
cv2.imshow('Grey', image_grey)
cv2.imshow("Gaussian blur", cv2.GaussianBlur(image_color, GaussianBlurVariables(51)[0], GaussianBlurVariables()[1]))
cv2.imshow("edges", cv2.Canny(image_grey, edgeParameters(100)[0], edgeParameters(0,100)[1]))
cv2.waitKey(0)  