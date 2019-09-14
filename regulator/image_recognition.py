import numpy as np
import cv2# as cv
#import matplotlib.pyplot as plt
img1 = cv2.imread('0.png', cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)



def findCircle(img):
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    height = np.size(img, 0)
    width = np.size(img, 1)
    dw = 300
    resized = cv2.resize(img, (dw, int(dw/width * height)))

    coeff = width / dw


    circles = cv2.HoughCircles(resized, cv2.HOUGH_GRADIENT, 1.2, 100)

    biggest_circle = (0, 0, 0)

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        #
        # def byRadius(_x, _y, r):
        #     return r

        np.sort(circles, )

        biggest_circle = circles[0]

        print(circles)

        # # loop over the (x, y) coordinates and radius of the circles
        # for (x, y, r) in circles:
        #     # draw the circle in the output image, then draw a rectangle
        #     # corresponding to the center of the circle
        #     cv2.circle(resized, (x, y), r, (0, 255, 0), 4)
        #     cv2.rectangle(resized, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    biggest_circle = biggest_circle[0] * coeff, biggest_circle[1] * coeff, biggest_circle[2] * coeff

    return resized, biggest_circle


def findColor(img, lower, upper):

    green = cv2.inRange(hsv, lower, upper)

    kernal = np.ones((5 ,5), "uint8")
    blue=cv2.dilate(green, kernal)
    res=cv2.bitwise_and(img1, img1, mask = blue)

    #cv2.imshow("", res)

    (_, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x = 0
    y = 0
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 100):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 3)

    return x, y

#magenta_lower = np.array([22,60,200],np.uint8)
#magenta_upper = np.array([60,255,255],np.uint8)
green_lower = np.array([50, 60, 60], np.uint8)
green_upper = np.array([80, 150, 150], np.uint8)

magenta_lower = np.array([150, 100, 30],np.uint8)
magenta_upper = np.array([165, 500, 500],np.uint8)


sens = 50
white_lower = np.array([0,20,255-sens], np.uint8)
white_upper = np.array([255,sens,255], np.uint8)

resized, circle = findCircle(gray)
x, y, r = (int(x) for x in circle)


cv2.circle(img1, (x, y), r, (0, 255, 0), 4)
cv2.rectangle(img1, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

findColor(hsv, green_lower, green_upper)

findColor(hsv, magenta_lower, magenta_upper)

findColor(hsv, white_lower, white_upper)

cv2.namedWindow("Color Tracking1")
cv2.imshow("Color Tracking1", img1)

#cv2.namedWindow("Color Tracking")
#cv2.imshow("Color Tracking", res)
cv2.waitKey()
