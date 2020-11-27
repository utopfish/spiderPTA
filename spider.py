# -*- coding: utf-8 -*-
"""
@Project : spiderPTA
@File    : spider.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/11/27 16:38
"""
import time
import re
import random
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from  dirtyWork import FindPic
class PTA():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1366, 768)

    def run(self,url,account,password):
        self.driver.get(url)  # 打开浏览器

        #TODO: 加入由于网页加载慢导致的错误的错误处理
        wait_time=5
        ## 定位账号，密码输入位置，输入账号密码
        accountBoxElem = WebDriverWait(self.driver, wait_time, 0.5). \
            until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))

        ActionChains(self.driver).move_to_element(accountBoxElem). \
            click(accountBoxElem).send_keys(account).perform()


        passwordBoxElem = WebDriverWait(self.driver, wait_time, 0.5). \
            until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))

        ActionChains(self.driver).move_to_element(passwordBoxElem). \
            click(passwordBoxElem).send_keys(password).perform()

        # 登录按钮
        Loginlement = self.driver.find_element_by_xpath('//*[@id="sparkling-daydream"]/div[3]/div/div[2]/form/div[2]/button/div/div')
        Loginlement.click()

        # 等待验证窗口可见
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="yidun_modal"]')))

        # 模拟拖动
        self.analogDrag()



    def analogDrag(self):

        # 获取图片地址和位置坐标列表
        while True:
            bgImageUrl =self.driver.find_element_by_xpath('//img[@class="yidun_bg-img"]').get_attribute("src")
            jiasawImageUrl=self.driver.find_element_by_xpath('//img[@class="yidun_jigsaw"]').get_attribute("src")
            self.saveImage(bgImageUrl,"bg")
            self.saveImage(jiasawImageUrl,"jiasaw")
            time.sleep(1)
            bgImagePath = 'pic/bg.png'
            jiasawPath = 'pic/jiasaw.png'
            try:
                distance = FindPic(bgImagePath,jiasawPath)
                break
            except Exception as e:
                print(e)
                print("刷新图片重新验证")
                self.startMove(20)
                time.sleep(2)

        #TODO: 对距离获取成功，滑块拖动失败状态进行确定，并重新验证
        self.startMove(distance)

    # 滑块拖动方法过于丑陋，但暂时能用
    def startMove(self, distance):
        element = self.driver.find_element_by_xpath('//div[@class="yidun_slider"]')

        # # 使用滑块的一半进行偏移设置
        # distance -= element.size.get('width') / 2
        # distance += 15

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 20:
                # 如果距离大于20，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()


    def saveImage(self,imageUrl,name):
        res = requests.get(imageUrl)
        if res.status_code == 200:
            open('pic/{}.png'.format(name), 'wb').write(res.content)  # 将内容写入图片
            print("done")




if __name__ == '__main__':
    url ='https://pintia.cn/problem-sets/1330901882209357824/submissions'
    account = '290970344@qq.com'
    password = 'nwuipmi2020'
    h = PTA()
    h.run(url,account,password)

