# Source: https://medium.com/@mrhwick/simple-lane-detection-with-opencv-bfeb6ae54ec0

import cv2
import numpy as np
import utils
import math


def get_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def get_blur(img):
    return cv2.GaussianBlur(img, (21, 21), 0)


def get_canny(img):
    return cv2.Canny(img, 50, 100)


def get_lines(img):
    return cv2.HoughLinesP(img, 1, np.pi / 180, 30)


def get_cropped(img, vertices):
    mask = np.zeros_like(img)
    channel_count = img.shape[2]
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def get_white(img):
    white_threshold = 200
    lower_white = np.array([white_threshold, white_threshold, white_threshold])
    upper_white = np.array([255, 255, 255])
    white_mask = cv2.inRange(img, lower_white, upper_white)
    white_image = cv2.bitwise_and(img, img, mask=white_mask)
    return white_image


def get_line(img):
    w = utils.width
    h = utils.height

    white = get_white(img)

    gray = get_gray(white)
    blur = get_blur(gray)
    canny = get_canny(blur)
    lines = get_lines(canny)

    x = []
    y = []
    flag = False

    if(lines != None):
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                x.extend([x1, x2])
                y.extend([y1, y2])
                flag = True

    min_y = int(img.shape[0] * 0.6)
    max_y = int(img.shape[0])

    font = cv2.FONT_HERSHEY_SIMPLEX

    if flag:
        poly = np.poly1d(np.polyfit(
            y,
            x,
            deg=1
        ))

        x_start = int(poly(max_y))
        x_end = int(poly(min_y))

        dx = int((x_end - x_start) * 0.23)
        dy = int(max_y - min_y)

        # Get radian of angle, and converts it to degree
        dir = math.atan2(dy, dx) / math.pi * 180 - 90
        dir = -dir

        cv2.line(img, (x_start, min_y), (x_end, max_y), (0, 255, 0), 2)

        if(dir > 0):
            cv2.putText(img, 'Right', (10, h - 10), font,
                        1, (255, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(img, 'Left', (10, h - 10), font,
                        1, (255, 0, 255), 2, cv2.LINE_AA)

        img = cv2.resize(img, (w * 2, h * 2))

        return {'angle': dir, 'image': img}
    else:
        cv2.putText(img, 'No way', (10, h - 10), font,
                    1, (255, 0, 255), 2, cv2.LINE_AA)
        img = cv2.resize(img, (w * 2, h * 2))
        return {'image': img}
