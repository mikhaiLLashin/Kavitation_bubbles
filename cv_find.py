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
    output = []
    high = 255
    first = True
    low = 1
    x = 100
    while (low > 0):
        low = high - x
        if (first == False):
            to_be_black_again_low = np.array([high])
            to_be_black_again_high = np.array([255])
            curr_mask = cv2.inRange(image, to_be_black_again_low,
                                    to_be_black_again_high)
            image[curr_mask > 0] = (0)
        ret, threshold = cv2.threshold(image, low, 255, cv2.THRESH_BINARY_INV)
        i, contours, hirerchy = cv2.findContours(threshold,
                                              cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        if (len(contours) > 0):
            output.append([cv2.contourArea(contours[0])])
            if (output[-1][0] < 10000):
                for i in range(len(contours)):
                    if len(contours[i]) > 300 and len(contours[i]) < 1000:
                        cv2.drawContours(im, contours[i], -1, (0, 0, 255), 3)
        high -= x
        first = False
    viewImage(im)
    return output

x = os.walk(r'C:\Users\lashi\Desktop\Cav_d\data\test\5_ alcohol')
for r, d, f in x:
    for i in range(1000):
        print(r + "\\" + str(f[i]))
        image = cv2.imread(r + "\\" + str(f[i]))
        print(get_area_of_each_gray_level(image))
