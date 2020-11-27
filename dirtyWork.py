# -*- coding: utf-8 -*-
"""
@Project : spiderPTA
@File    : dirtyWork.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/11/27 17:37
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np


def changeTemp(img):
    max_row = np.max(img,axis=1)
    max_col = np.max(img,axis=0)
    for i in range(len(img)):
        if max_row[i]!=0:
            top =i
            break
    for i in range(len(img)-1,-1,-1):
        if max_row[i]!=0:
            bottom = i
            break
    for i in range(len(img[0])):
        if max_col[i]!=0:
            left= i
            break
    for i in range(len(img[0])-1,-1,-1):
        if max_col[i] !=0:
            right= i
            break
    return img[top:bottom,left:right],left

def FindPic(target, template):
    """
    找出图像中最佳匹配位置
    :param target: 目标即背景图
    :param template: 模板即需要找到的图
    :return: 返回最佳匹配对应的坐标，以及目标在原始透明背景中的偏移量
    """


    img_rgb = cv2.imread(target)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    template,left= changeTemp(template)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = res.max()
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    plt.imshow(img_rgb)
    plt.show()
    return loc[1][0]+left



if __name__=="__main__":
    bgImagePath='pic/bg.png'
    jiasawPath='pic/jiasaw.png'

    print(FindPic(bgImagePath,jiasawPath))