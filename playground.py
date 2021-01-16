import cv2 as cv

img = cv.imread('Photos/Hey.png')

cv.imshow('Cat', img)

cv.waitKey(0)
