# coding:utf-8
import os
import random
import numpy as np
from PIL import Image
from captcha.image import ImageCaptcha

NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LOW_CASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
UP_CASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
# CAPTCHA_LIST = NUMBER + LOW_CASE + UP_CASE
CAPTCHA_LIST = NUMBER
CAPTCHA_LEN = 4
CAPTCHA_HEIGHT = 30
CAPTCHA_WIDTH = 100


def random_captcha_text(char_set=CAPTCHA_LIST, captcha_size=CAPTCHA_LEN):
    '''
    随机生成验证码文本
    :param char_set:
    :param captcha_size:
    :return:
    '''
    captcha_text = [random.choice(char_set) for _ in range(captcha_size)]
    return ''.join(captcha_text)


def gen_captcha_text_and_image(path=None):
    '''
    生成随机验证码
    :param width:
    :param height:
    :param save:
    :return: np数组
    '''
    # image = ImageCaptcha(width=width, height=height)
    # image = Image.open('D:\\jxfilterpic\\8465.jpg')
    # 验证码文本
    # captcha_text = random_captcha_text()
    # captcha = image.generate(captcha_text)
    # 保存
    # if save: image.write(captcha_text, captcha_text + '.jpg')
    # captcha_image = Image.open(captcha)
    # 转化为np数组
    # captcha_image = np.array(captcha_image)
    # captcha_image = np.array(image.getdata()).reshape(30, 100, -1)
    # return '8465', captcha_image

    filepath = []
    filename = []
    for root, dirs, files in os.walk(path):
        for n in files:
            filepath.append(root + os.sep + n)
            name = n.replace('.jpg', '')
            filename.append(name)
    index = random.randint(0, len(filepath)-1)

    image = Image.open(filepath[index])
    captcha_image = np.array(image.getdata()).reshape(30, 100, -1)
    captcha_text = filename[index]
    return captcha_text, captcha_image


def get_filter_pic(path=None):
    image = Image.open(path)
    captcha_image = np.array(image.getdata()).reshape(30, 100, -1)
    return captcha_image


if __name__ == '__main__':
    t, im = gen_captcha_text_and_image()
    print(t, im)
    print(im.shape)
