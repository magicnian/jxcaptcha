#!/usr/local/bin/python
# -*- coding: utf8 -*-

import cv2

import sys


indexstr = sys.argv[1]
print('验证码位置：', indexstr)

img = cv2.imread(indexstr)
GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(GrayImage, (5, 5), 0)  # 高斯滤波
ret, thresh3 = cv2.threshold(blurred, 165, 255, cv2.THRESH_BINARY)
cv2.imwrite('E:\\jxfilterpic\\test.jpg', thresh3)



