#Produces a huge ass picture
import cv2
img = cv2.imread("puppy.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,47,255,cv2.THRESH_BINARY)
cv2.imshow("thresh",thresh) #<-- grayscale image
#cv2.imshow("original",img)  <-- original image
cv2.waitKey(0)
