from tkinter import *
import cv2
import numpy as np
import math


def getMax(image):
    list = [i for i in range(0,256)]
    counts = dict()
    for i in range(len(list)):
        counts[list[i]]=0
    img = cv2.imread(image)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
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
    print(pressure)
    if pressure > 140:
        return"Low pressure --> you are easy going and chill!"
    elif pressure > 90:
        return"Medium pressure --> you are boring:("
    else:
        return"High pressure --> you have strong emotions and are quick to reactXD"

def sizeAnalysis(imageName):
    UL, LR = getSize(imageName)
    textH = abs(UL[1] - LR[1])
    textW = abs(UL[0] - LR[0])
    mid = 3
    if textH + textW < mid:
        return "Small handwriting --> you have strong focus and concentration and you are introverted!"
    else:
        return "Large handwriting --> you are people oriented and want to be noticed!"

def getSlant(image):
    im = cv2.imread(image)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    sumDif = 0
    for i in range(1,len(contours)):
        cnt = contours[i]
        img = cv2.drawContours(im,cnt,-1,(0,0,255),1)
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
        avDif = (rightmost[0] - leftmost[0])/2 + leftmost[0]
        sumDif += avDif
        img = cv2.rectangle(img,(leftmost[0],topmost[1]),(rightmost[0],bottommost[1]),(0,255,0),2)
    avSumDif = int(sumDif//len(contours))
    middle = int(img.shape[1]//2)
    difference = middle - avSumDif
    if difference < -15:
        return "Leftward slant --> you are rebellious and like to work alone>:)"
    elif difference > 15:
        return "Rightward slant --> you are a social butterfly!"
    else:
        return "No slant --> you are logical and practical!"
        
def getGray(value):
    R = value[0]
    G = value[1]
    B = value[2]
    return round((R + G + B) / 3)

def getSize(imageName):
    #3x5 index card
    img = cv2.imread(imageName)
    pixelRows = img.shape[0]
    pixelCols = img.shape[1]
    pixelSize = 5 / pixelCols
    initialGray = getGray(img[0][0])
    UL = [pixelCols, pixelRows]
    LR = [0,0]
    for i in range(pixelCols):
        for j in range(pixelRows):
            value = img[j][i]
            gray = getGray(value)
            if gray < initialGray - 20:
                posUL = [j, i]
                if sum(posUL) < sum(UL):
                    UL = posUL
    for i in range(pixelCols-1, 0, -1):
        for j in range(pixelRows-1, 0, -1):
            value = img[j][i]
            gray = getGray(value)
            if gray < initialGray - 20:
                posLR = [j, i]
                if sum(posLR) > sum(LR):
                    LR = posLR
    UL[0] *= pixelSize
    UL[1] *= pixelSize
    LR[0] *= pixelSize
    LR[1] *= pixelSize
    return (UL, LR)

def roundness(image):
    #set maxRadius equal to half the linesize 
    img = cv2.imread(image,0)
    img = cv2.medianBlur(img,5)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=40)
    circles = np.uint16(np.around(circles))
    numCircles = 0
    for i in circles[0,:]:
        numCircles += 1
    print(numCircles)

def handwriting(image):
    pressure = pressureAnalyzer(image)
    size = sizeAnalysis(image)
    slant = getSlant(image)
    result = "Your results: \n" + pressure + "\n" + size + "\n" + slant
    return result

def makeResultsPretty(canvas, width, height, image):
    analysis = handwriting(image)
    canvas.create_rectangle(0, 0, width, height, fill = "light blue")
    canvas.create_text(width // 2, height // 2, text = analysis) #handwriting

def draw(canvas, width, height, image):
    makeResultsPretty(canvas, width, height, image)

def runDrawing(image, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    draw(canvas, width, height, image)
    root.mainloop()
    print("bye!")

image = input("Give me the image name ---> ")
runDrawing(image, 500, 100)