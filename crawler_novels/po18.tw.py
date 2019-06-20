# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/18 12:39'

'''
https://members.po18.tw/apps/login.php
'''

import random
import requests
import time
import os
import re
from collections import OrderedDict
from bs4 import BeautifulSoup

from selenium import webdriver
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CHROME_PATH = r"{0}/resource/{1}".format(BASE_DIR, r"Chrome/App/Google Chrome")
CONFIG_INFO_FILE = r"{0}/{1}".format(BASE_DIR, "Config.ini")
SCREEN_PATH = r"{0}/{1}/{2}".format(BASE_DIR, "resource", "screenshots")

if not os.path.exists(SCREEN_PATH):
    os.makedirs(SCREEN_PATH)

chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = "{0}/{1}".format(CHROME_PATH, "chrome.exe")
chromeDriver = "{0}/{1}".format(CHROME_PATH, "chromedriver.exe")
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--disable-gpu')
browerLength = 1280
browerWidth = 4096
driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chromeOptions)
driver.set_window_size(browerLength, browerWidth)

# 单一小说网址
DOWN_FLODERS = r"E:\下载小说"

def rtn_chapter_list_info(html):

    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"class": "bookbox"})[0].h1.text
    # novelName = novelName.replace("\n", "")
    novelName = novelName.strip()
    novelName = novelName.split("《")[1]
    novelName = novelName.split("》")[0]
    print(novelName)

    chapterListInfoSoup = soup.find_all(name="select", attrs={"id": "Page_select"})[0].find_all(name="option")

    chapterListInfoArr = []

    for ddItem in chapterListInfoSoup:

        # print(str(ddItem))
        patt = re.compile(r'<option value="/(.+?)">(.+?)</option>')
        option = patt.findall(str(ddItem))
        # print(option)
        chapterListInfoDict = OrderedDict()
        chapterListInfoDict["text"] = option[0][1]
        chapterListInfoDict["href"] = option[0][0]
        # print(chapterListInfoDict)

        chapterListInfoArr.append(chapterListInfoDict)

    return chapterListInfoArr, novelName

def rtn_chapter_txt(chapterHtml):

    soup = BeautifulSoup(chapterHtml, 'html.parser')

    txtContent = soup.find_all(name="div", attrs={"class": "read-txt"})[0].text

    # txtContent = str(txtContent).replace("<br/>", "\n")

    # print(txtContent)
    # time.sleep(2000)
    # txtContent = BeautifulSoup(txtContent, 'html.parser').text
    # # txtContent = txtContent.text
    # txtContent = txtContent.replace(' ', '')
    # txtContent = txtContent.replace('　　', '')
    # txtContent = txtContent.replace('本书由本站首发，请勿转载！◎思◎兔◎在◎线◎阅◎读◎', '')
    # txtContent = txtContent.replace('本书由本站首发，请勿转载！', '')
    # txtContent = txtContent.replace('本书由首发，请勿转载！', '')
    # txtContent = txtContent.replace('()', '')
    # txtContent = txtContent.replace('*作*品*由*思*兔*在*線*閱*讀*網*友*整*理*上*傳*', '')
    # txtContent = txtContent.replace('严禁附件中包含其他网站的广告本文已阅读完毕，欢迎发表书评！', '')
    # txtContent = txtContent.replace('(adsbygoogle = window.adsbygoogle || []).push({});', '')
    # txtContent = txtContent.replace('(adsbygoogle=window.adsbygoogle||[]).push({});', '')
    # txtContent = txtContent.replace('\n\n', '\n')
    # txtContent = txtContent.replace('\n\n', '\n')
    # txtContent = txtContent.replace('\n\n', '\n')
    # txtContent = txtContent.replace('\n\n', '\n')
    # txtContent = txtContent.replace('\n\n\n', '\n')
    # txtContent = txtContent.replace('☆、', '\n')
    # txtContent = txtContent.replace('\ue4c6','')
    # txtContent = txtContent.replace('\ue0d8','')
    # print(txtContent)

    return txtContent

def write_txt_content(txtFileName, chapterName, chapterTxt):
    with open(txtFileName, 'a', encoding="utf-8") as f:
        f.write(chapterName + "\n")
        chapterTxt = chapterTxt.replace(chapterName, "")
        f.write(chapterTxt + "\n\n")

def login_get_url(url):
    print("开始获取页面：{0}".format(url))
    driver.get(url)
    driver.implicitly_wait(30)
    loginPageShotFileName = "loginUrl.png"
    driver.find_element_by_name("account").send_keys("slovent")
    driver.find_element_by_name("pwd").send_keys("11111111")
    driver.find_element_by_class_name("btn_func").click()
    driver.implicitly_wait(30)
    driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))
    return driver

def get_url(driver, url):
    print("开始获取页面：{0}".format(url))
    driver.get(url)
    driver.implicitly_wait(30)
    loginPageShotFileName = "curr_page.png"
    driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))
    return driver

def get_chapter_html(driver, chapterListInfo):
    print("开始获取页面：{0}".format(chapterListInfo["href"]))
    driver.get(chapterListInfo["href"])
    driver.implicitly_wait(30)

    waitMaxSecond = 120
    loopCount = 5

    while True:

        loopCount -= 1
        xpath = '//*[@id="readmask"]/div/h1'
        isXpath = IsElementExistClick(driver, xpath)

        if isXpath is True:
            break
        elif loopCount == 0:
            loopCount = 5
            print("重新获取页面：{0}".format(chapterListInfo["href"]))
            driver.get(chapterListInfo["href"])
            driver.implicitly_wait(30)
        else:
            print(loopCount, "正在等待5秒后重试！")
            time.sleep(5)

    loginPageShotFileName = "{0}.png".format(chapterListInfo["text"])
    driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))
    return driver.page_source

def IsElementExistClick(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath).click()
        return True
    except:
        return False

def rtn_chapter_list_info(driver, urls):
    chapterListInfoAll = []

    for url in urls:
        print("开始获取页面：{0}".format(url))
        driver.get(url)
        driver.implicitly_wait(30)
        loginPageShotFileName = "curr_page.png"
        driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))

        rtnStrHtml = driver.page_source
        soup = BeautifulSoup(rtnStrHtml, 'html.parser')
        soupChapterListInfos = soup.find_all(name="div", attrs={"class": "l_chaptname"})
        for soupChapterListInfo in soupChapterListInfos:
            chapterListInfoDict = OrderedDict()

            chapterListInfoDict["text"] = soupChapterListInfo.a.text
            chapterListInfoDict["href"] = "{0}{1}".format("https://www.po18.tw", soupChapterListInfo.a["href"])
            chapterListInfoAll.append(chapterListInfoDict)

    return chapterListInfoAll

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def rtn_str_html_new(driver, url):
    print("开始获取页面：{0}".format(url))
    driver.get(chapterListInfo["href"])
    driver.implicitly_wait(30)

    waitMaxSecond = 120
    loopCount = 5

    loginPageShotFileName = "{0}.png".format(chapterListInfo["text"])

    while True:

        loopCount -= 1
        xpath = '//*[@id="readmask"]/div/h1'
        isXpath = IsElementExistClick(driver, xpath)

        if isXpath is True:
            break
        elif loopCount == 0:
            loopCount = 5
            print("重新获取页面：{0}".format(chapterListInfo["href"]))
            driver.get(chapterListInfo["href"])
            driver.implicitly_wait(30)
        else:
            print(loopCount, "正在等待5秒后重试！")
            driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))
            time.sleep(5)

    driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))
    return driver.page_source



if __name__ == '__main__':

    try:

        loginUrl = "https://members.po18.tw/apps/login.php"
        driver = login_get_url(loginUrl)

        rootUrl = "https://www.po18.tw/books" # 网站根目录
        novelId = "679517"
        fullNovelUrl = "{0}/{1}".format(rootUrl, novelId)
        driver = get_url(driver, fullNovelUrl)

        chapterHtmlPath = '//div[@class="toolbar"]/a[2]'
        # driver.find_element_by_xpath(chapterHtmlPath)
        driver.find_element_by_xpath(chapterHtmlPath).click()
        driver.implicitly_wait(30)
        loginPageShotFileName = "curr_page.png"
        driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))

        strHtml = driver.page_source

        soup = BeautifulSoup(strHtml, 'html.parser')
        novelName = soup.find_all(name="h1", attrs={"class": "book_name"})[0].text
        print(novelName)

        # 取页面最大值
        pageMaxNumTemp = soup.find_all(name="a", attrs={"class" : "num"})
        num = []
        for x in pageMaxNumTemp:
            numStr = x.text
            if is_number(numStr) is True:
                num.append(int(numStr))
        if num:
            maxNum = max(num)
        else:
            maxNum = 1

        pageUrls = []
        for i in range(1, maxNum + 1):
            pageUrl = "https://www.po18.tw/books/{0}/articles?page={1}".format(novelId, i)
            pageUrls.append(pageUrl)
        chapterListInfos = rtn_chapter_list_info(driver, pageUrls)

        novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)
        if os.path.exists(novelFilePath):
            os.remove(novelFilePath)

        for chapterListInfo in chapterListInfos:
            strChapterHtml = get_chapter_html(driver, chapterListInfo)
            chapterTxt = rtn_chapter_txt(strChapterHtml)
            print(chapterTxt)
            print("路径：{0}，正在获取 章节：{1} ！！！".format(novelFilePath, chapterListInfo["text"]))
            write_txt_content(novelFilePath, chapterListInfo["text"], chapterTxt)

    except Exception as e:
        print(e)
        loginPageShotFileName = "main_err.png"
        driver.save_screenshot("{0}/{1}".format(SCREEN_PATH, loginPageShotFileName))