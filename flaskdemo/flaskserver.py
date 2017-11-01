#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import cv2
import time
from captchaCnn import captcha_cnn
import tensorflow as tf
import numpy as np
from captchaCnn.cnn_train import cnn_graph
from captchaCnn.captcha_cnn import vec2text
from captchaCnn.util import CAPTCHA_LIST, CAPTCHA_WIDTH, CAPTCHA_HEIGHT, CAPTCHA_LEN

from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
# app.config中的config是字典的子类，可以用来设置自有的配置信息，也可以设置自己的配置信息
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}
static_config = {'filterpic': 'static' + os.sep + 'filterpic'}


# For a given file, return whether it's an allowed type or not
# 函数allowed_file(filename)用来判断filename是否有后缀以及后缀是否在app.config['ALLOWED_EXTENSIONS']中
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


x = tf.placeholder(tf.float32, [None, 30 * 100])
keep_prob = tf.placeholder(tf.float32)
y_conv = cnn_graph(x, keep_prob, (30, 100))
saver = tf.train.Saver()
sess = tf.Session()
print(tf.train.latest_checkpoint('D:\\jxcaptcha\\captchaCnn'))
saver.restore(sess, tf.train.latest_checkpoint('D:\\jxcaptcha\\captchaCnn'))


@app.route('/test', methods=['GET'])
def verifypic():
    path = request.args['path']
    print('path:', path)
    img = cv2.imread(path)
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(GrayImage, (5, 5), 0)  # 高斯滤波
    ret, thresh3 = cv2.threshold(blurred, 165, 255, cv2.THRESH_BINARY)
    cv2.imwrite('E:\\jxfilterpic\\test.jpg', thresh3)

    time.sleep(0.5)

    # pre_text = captcha_cnn.verifypic(path='E:\\jxfilterpic\\test.jpg')

    text, image = captcha_cnn.gen_captcha_text_and_image(path='C:\\Users\\liunn\\Desktop\\pic')
    image = image.flatten() / 255
    pre_text = captcha_cnn.captcha2text([image])
    return jsonify({'result': pre_text})


@app.route('/captchaverify', methods=['POST'])
def captchaverify():
    # 第一步获取上传的图片，并且存到本地
    # 客户端上传的图片必须pic标识
    # upload_file是上传文件对应的对象
    upload_file = request.files['pic']
    if upload_file and allowed_file(upload_file.filename):
        # 判断文件名是否安全，例如防止文件名是../../../a.png
        filename = secure_filename(upload_file.filename)
        # app.root_path获取flaskserver.py所在目录在文件系统中的绝对路径
        # 函数os.path.join()用来将使用合适的路径分隔符将路径组合起来
        filepath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
        upload_file.save(filepath)
        return verify(filepath)
    else:
        return 'hello, image upload failed!'


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

    predict = tf.argmax(tf.reshape(y_conv, [-1, CAPTCHA_LEN, len(CAPTCHA_LIST)]), 2)
    vector_list = sess.run(predict, feed_dict={x: [image], keep_prob: 1})
    vector_list = vector_list.tolist()
    text_list = [vec2text(vector) for vector in vector_list]
    return jsonify({'result': text_list})


if __name__ == '__main__':
    app.run(debug=True, port=8333)
