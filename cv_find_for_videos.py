import cv2
import numpy as np
import os

def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)

def get_area_of_each_gray_level(im):
    ## convert image to gray scale (must br done before contouring)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 55, 255, 0)
    output = []
    high = 255
    first = True
    low = 1
    x = 15
    while (low > 0):
        low = high - x
        ret, threshold = cv2.threshold(image, low, 255, cv2.THRESH_BINARY_INV)
        i, contours, hirerchy = cv2.findContours(threshold,
                                              cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        if (len(contours) > 0):
            for i in range(len(contours)):
                if len(contours[i]) > 500 and cv2.contourArea(contours[i]) > 10000:
                    print(cv2.contourArea(contours[i]))
                    M = cv2.moments(contours[i])
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    im = cv2.circle(im, (cX,cY), radius=0, color=(0, 255, 0), thickness=10)
                    cv2.drawContours(im, contours[i], -1, (0, 0, 255), 3)
        high -= x
        first = False
    viewImage(im)

x = r"C:\Users\lashi\Desktop\Cav_d\videos\50_.mp4"
vid = cv2.VideoCapture(x)
while (vid.isOpened()):
    ret, frame = vid.read()
    get_area_of_each_gray_level(frame)