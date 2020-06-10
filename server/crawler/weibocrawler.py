from selenium import webdriver
import time
import re

#全局变量
driver = webdriver.Chrome("F:\chromedriver\chromedriver.exe")


def loginWeibo(username, password):
    driver.get('https://weibo.cn')
    time.sleep(3)

    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    #这里只是看一下cookie内容，下面不会用到这个cookie值，因为driver会把cookie自动带过去
    cookies = driver.get_cookies()
    cookie_list = []
    for dict in cookies:
        cookie = dict['name'] + '=' + dict['value']
        cookie_list.append(cookie)
    cookie = ';'.join(cookie_list)
    print (cookie)

    #driver.close()

if __name__ == '__main__':
    username = input()            # 输入微博账号
    password = input()             # 输入密码
    loginWeibo(username, password)      # 要先登录，否则抓取不了微博内容