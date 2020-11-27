# -*- coding: utf-8 -*-
"""
@Project : spiderPTA
@File    : baseTest.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/11/27 16:46
"""
# 测试selenium是否能用
from selenium import webdriver
driver=webdriver.Chrome()

driver.get("http://www.baidu.com")
