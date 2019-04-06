import cv2

img = cv2.imread("ImageName.jpg")
edges = cv2.Canny(img, 100, 1000)
#Display edges
cv2.imshow('WindowNameHere', edges)
cv2.waitKey(0)