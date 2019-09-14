import numpy as np
import cv2# as cv
#import matplotlib.pyplot as plt
img1 = cv2.imread('0.png', cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

#magenta_lower = np.array([22,60,200],np.uint8)
#magenta_upper = np.array([60,255,255],np.uint8)
green_lower = np.array([50, 60, 60], np.uint8)
green_upper = np.array([80, 150, 150], np.uint8)

green = cv2.inRange(hsv, green_lower, green_upper)

kernal = np.ones((5 ,5), "uint8")
blue=cv2.dilate(green, kernal)
res=cv2.bitwise_and(img1, img1, mask = green)

(_, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 300):
        x, y, w, h = cv2.boundingRect(contour)
        img = cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 3)

cv2.namedWindow("Color Tracking1")
cv2.imshow("Color Tracking1", img1)

cv2.namedWindow("Color Tracking")
cv2.imshow("Color Tracking", res)
cv2.waitKey()
