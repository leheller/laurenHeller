"""
import cv2

img = cv2.imread("puppy.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,47,255,cv2.THRESH_BINARY)
cv2.imshow("thresh",thresh) #<-- grayscale image
#cv2.imshow("original",img)  <-- original image
cv2.waitKey(0)
"""
import cv2
import math
  
# importing library for plotting 
from matplotlib import pyplot as plt 
  
# reads an input image 
img = cv2.imread("puppy.jpg")
#cv2.imshow(img, 1)
# find frequency of pixels in range 0-255 
histr = cv2.calcHist([img],[0],None,[256],[0,256]) 
  



list = [i for i in range(0,256)]

counts = dict()
for i in range(len(list)):
    counts[list[i]]=0


def getMax(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(gray,47,255,cv2.THRESH_BINARY)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            value = gray[i][j]
            counts[value] += 1
    bestVal = 0
    for value in range(len(counts)):
        if counts[value] > bestVal and value < 200:
            bestVal = counts[value]
            bestKey = value
    return bestKey
    
def pressureAnalyzer(image):
    pressure = getMax(image)
    if pressure > 125:
        return("Low pressure -> you are easy going and chill")
    elif pressure > 75:
        return("Medium pressure -> you are boring:(")
    else:
        return("High pressure -> you have strong emotions and are quick to react")