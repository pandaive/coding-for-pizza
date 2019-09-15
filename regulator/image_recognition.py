import numpy as np
import cv2# as cv
import math
import time
#import matplotlib.pyplot as plt





def findCircle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height = np.size(img, 0)
    width = np.size(img, 1)
    dw = 200
    resized = cv2.resize(gray, (dw, int(dw/width * height)))

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

        #print(circles)

        # # loop over the (x, y) coordinates and radius of the circles
        # for (x, y, r) in circles:
        #     # draw the circle in the output image, then draw a rectangle
        #     # corresponding to the center of the circle
        #     cv2.circle(resized, (x, y), r, (0, 255, 0), 4)
        #     cv2.rectangle(resized, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    biggest_circle = biggest_circle[0] * coeff, biggest_circle[1] * coeff, biggest_circle[2] * coeff

    return resized, biggest_circle


def findColor(img, lower, upper):

    in_range = cv2.inRange(img, lower, upper)

    kernal = np.ones((5 ,5), "uint8")
    dilated=cv2.dilate(in_range, kernal)
    #res=cv2.bitwise_and(img, img, mask = dilated)

    (_, contours, hierarchy) = cv2.findContours(in_range, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_x = 0
    max_y = 0
    max_area = 0
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        if area > max_area:
            x, y, w, h = cv2.boundingRect(contour)
            max_area = area
            max_x = x
            max_y = y

    return max_x, max_y



circles = []
circles_i = 0

def get_angle(img):
    start = time.time()
    height = np.size(img, 0)
    width = np.size(img, 1)
    global circles_i
    #global max_circle
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #magenta_lower = np.array([22,60,200],np.uint8)
    #magenta_upper = np.array([60,255,255],np.uint8)
    green_lower = np.array([50, 60, 60], np.uint8)
    green_upper = np.array([80, 150, 150], np.uint8)

    magenta_lower = np.array([150, 100, 30], np.uint8)
    magenta_upper = np.array([165, 500, 500], np.uint8)


    sens = 70
    white_lower = np.array([0,0,255-sens], np.uint8)
    white_upper = np.array([255,sens,255], np.uint8)

    if len(circles) > 5 or circles_i % 30 == 0:
        resized, circle = findCircle(img)
        x, y, r = (int(x) for x in circle)

        circles.append((x, y, r))
        circles_i += 1

    max_circle = (int(width/2), int(height/2), int(height/2))

    cirles_max_len = 20
    if len(circles) > cirles_max_len:
        print("Popping {} values".format(len(circles) - cirles_max_len))
        for i in range(len(circles) - cirles_max_len):
            circles.pop(0)

    for circle in circles:
        x, y, r = circle
        if r > max_circle[2]:
            max_circle = (x,y,r)
        else:
            x, y, r = max_circle
    print((x, y, r))
    #x, y, r = ()

    height,width,depth = img.shape
    circle_img = np.zeros((height,width), np.uint8)
    cv2.circle(circle_img,(x,y),r,1,thickness=-1)

    masked_data = cv2.bitwise_and(img, img, mask=circle_img)

    masked_data_hsv = cv2.cvtColor(masked_data, cv2.COLOR_BGR2HSV)

    g_rect = findColor(masked_data_hsv, green_lower, green_upper)

    m_rect = findColor(masked_data_hsv, magenta_lower, magenta_upper)

    w_rect = findColor(masked_data_hsv, white_lower, white_upper)

    y_m_d = m_rect[1] - y
    x_m_d =  m_rect[0] - x
    m_angle = math.atan2(y_m_d,x_m_d) * 360 / (2*math.pi)
    m_angle = 360 - (-m_angle) + 90
    #print("y {} x {} angle {}".format(y_m_d, x_m_d, m_angle))

    y_g_d = g_rect[1] - y
    x_g_d = g_rect[0] - x
    g_angle = math.atan2(y_g_d,x_g_d) * 360 / (2*math.pi)
    g_angle = 360 - (-g_angle) + 90

    # print("y {} x {} angle {}".format(y_g_d, x_g_d, g_angle))
    #
    cv2.rectangle(masked_data, (g_rect[0], g_rect[1]), (g_rect[0]+10, g_rect[1]+10), (255, 0, 0), 3)
    cv2.rectangle(masked_data, (m_rect[0], m_rect[1]), (m_rect[0]+10, m_rect[1]+10), (255, 0, 0), 3)
    cv2.rectangle(masked_data, (w_rect[0], w_rect[1]), (w_rect[0]+10, w_rect[1]+10), (255, 0, 0), 3)
    #

    # cv2.namedWindow("Color Tracking")
    # cv2.imshow("Color Tracking", masked_data)
    # cv2.waitKey()

    end = time.time()

    #print("get_angle {}".format(end - start))

    return g_angle - 180 - m_angle, masked_data


if __name__ == "__main__":
    image = cv2.imread('../images/output1out1.png', cv2.IMREAD_COLOR)

    print(get_angle(image))