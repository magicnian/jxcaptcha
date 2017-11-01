#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import time

from flask import jsonify

from captchaCnn import captcha_cnn

static_config = {'filterpic': 'static' + os.sep + 'filterpic'}


def verify(path=None):
    img = cv2.imread(path)
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(GrayImage, (5, 5), 0)  # 高斯滤波
    ret, thresh3 = cv2.threshold(blurred, 165, 255, cv2.THRESH_BINARY)
    # os.path.dirname(os.path.abspath(__file__))获取当前文件的绝对路径
    filepath = os.path.dirname(os.path.abspath(__file__))+os.sep+static_config['filterpic']+os.sep+'filter.png'
    cv2.imwrite(filepath, thresh3)

    time.sleep(0.5)

    image = captcha_cnn.get_filter_pic(path=filepath)
    image = image.flatten() / 255
    pre_text = captcha_cnn.captcha2text([image])
    return jsonify({'result': pre_text})