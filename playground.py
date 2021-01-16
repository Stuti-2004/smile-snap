import cv2 as cv

capture = cv.VideoCapture('Videos/Mask.mp4')

cv.imshow('Cat', capture)

cv.waitKey(0)
