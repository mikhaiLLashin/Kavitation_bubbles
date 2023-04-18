import cv2
import numpy as np
import os


def in_c(x, y, contour):
    result = cv2.pointPolygonTest(contour, (x, y), False)
    if (result == 1):
        return True
    else:
        return False


def mean_c(image, contour):
    s = 0
    k = 0
    step = 10
    xx, yy, w, h = cv2.boundingRect(contour)
    for y in range(min(yy, h), max(yy, h), step):
        for x in range(min(xx, w), max(xx, w), step):
            if (in_c(x, y, contour)):
                s += sum(image[y][x])
                k += 1
    return s / k if k != 0 else 0


def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(10)


def draw(im, cnt):
    ## convert image to gray scale (must br done before contouring)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 50, 255, 0)
    ret, threshold = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
    i, contours, hirerchy = cv2.findContours(threshold,
                                             cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    m = 0
    for c in contours:
        if (cv2.contourArea(c) > m):
            m = cv2.contourArea(c)
    m *= 0.7
    cnt = 0
    for i in range(len(contours)):

        if (cv2.contourArea(contours[i]) > 100 and mean_c(im, contours[i]) > 10) or cv2.contourArea(contours[i]) > m:
            if cv2.contourArea(contours[i]) < m:
                cnt += 1
            M = cv2.moments(contours[i])
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                im = cv2.circle(im, (cX, cY), radius=0, color=(0, 255, 255), thickness=10)
            except:
                pass
            mi = 100000
            ma = 0
            s = 0
            k = 0

            for point in contours[i]:
                x = point[0][0]
                y = point[0][1]
                mi = min(mi, ((x - cX) ** 2 + (y - cY) ** 2) ** 0.5)
                ma = max(ma, ((x - cX) ** 2 + (y - cY) ** 2) ** 0.5)
                s += ((x - cX) ** 2 + (y - cY) ** 2) ** 0.5
                k += 1
            mid = s / k
            cv2.circle(im, (cX, cY), round(mid), (0, 255, 0), 2)
            cv2.circle(im, (cX, cY), round(mi), (0, 255, 0), 2)
            cv2.circle(im, (cX, cY), round(ma), (0, 255, 0), 2)
            cv2.drawContours(im, contours[i], -1, (0, 0, 255), 3)
            cv2.putText(im, "Area: " + str(cv2.contourArea(contours[i])), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)
            cv2.putText(im, "Min dist: " + f"{mi:.{5}f}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(im, "Max dist: " + f"{ma:.{5}f}", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(im, "Mean dist: " + f"{mid:.{5}f}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            print("разность:", ma / mi if mi != 0 else 0)

    first = False
    viewImage(im)
    return cnt


x = r"C:\Users\lashi\Desktop\Cav_d\videos\0_.mp4"
vid = cv2.VideoCapture(x)
while (vid.isOpened()):
    ret, frame = vid.read()
    cnt = draw(frame, cnt)
