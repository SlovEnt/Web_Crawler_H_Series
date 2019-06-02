# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/11 9:26'

'''
https://www.mozhua.net/


'''


import time
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from selenium import webdriver
import os
import re
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CHROME_PATH = r"{0}\resource\{1}".format(BASE_DIR, "Chrome/App/Google Chrome/")
CONFIG_INFO_FILE = r"{0}\{1}".format(BASE_DIR, "Config.ini")
EXCEL_FILE = r"{0}\{1}".format(BASE_DIR, "课后测试题及答案.xlsx")

chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = "{0}/{1}".format(CHROME_PATH, "chrome.exe")
chromeDriver = "{0}/{1}".format(CHROME_PATH, "chromedriver.exe")
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--disable-gpu')
# driver.set_window_size(1280, 2048)

driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chromeOptions)


novelId = "read-113352-93478-1.html"  # 长相思(全集）
ROOT_URL = "https://www.mozhua.net/{0}".format(novelId)
print(ROOT_URL)
DOWN_FLODERS = r"E:\下载小说"

# 页面获取判断标志 正常html页面里的唯标识
INDEX_DOWN_FLAG = "txt_bg"
SUB_DOWN_FLAG = "txt_bg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
headers = {'Host': ROOT_URL}
headers = {'Referer': ROOT_URL}
headers = {'Upgrade-Insecure-Requests': '1'}

CHAPTER_ID = 0

with open(r"E:\下载小说\page.info", 'w', encoding="utf-8") as f:
    f.write(str(CHAPTER_ID))


def rtn_chapter_list_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"id": "txt_bg"})[0].h1.text
    if "《" in novelName:
        novelName = novelName.split("《")[1]
        novelName = novelName.split("》")[0]
    elif "-" in novelName:
        novelName = novelName.split("-")[0]
    novelName = novelName.strip()
    print("开始下载《{0}》".format(novelName))

    chapterListInfoSoup = soup.find_all(name="div", attrs={"class": "pages"})[0].find_all(name="a")

    chapterListInfoArr = []

    for ddItem in chapterListInfoSoup:

        chapterListInfoDict = OrderedDict()

        if "href" not in str(ddItem):
            continue

        chapterListInfoDict["text"] = ddItem.text
        chapterListInfoDict["href"] = ddItem["href"]
        print(chapterListInfoDict)

        chapterListInfoArr.append(chapterListInfoDict)

    return chapterListInfoArr, novelName


def rtn_chapter_txt(chapterHtml, txtFileName, chapterName):
    soup = BeautifulSoup(chapterHtml, 'html.parser')

    try:
        txtContent = soup.find_all(name="div", attrs={"id": "txt_content"})[0]

        newTxtContent = soup.find_all(name="p")

        for x in newTxtContent:

            txtLine = x.text

            if "" == txtLine:
                continue

            if ".qrlink" in txtLine:
                continue

            if "document" in txtLine:
                continue

            if "好文推荐" in txtLine:
                continue

            if "GMT+8" in txtLine:
                continue

            if "Processed" in txtLine:
                continue

            if "Memcache" in txtLine:
                continue

            if "Powered" in txtLine:
                continue

            if "魔爪小说阅读器" in txtLine:
                continue

            if "☆、" in txtLine:

                with open(r"E:\下载小说\page.info", 'r', encoding="utf-8") as f:
                    CHAPTER_ID = f.read()

                CHAPTER_ID_1 = int(CHAPTER_ID) + 1

                with open(r"E:\下载小说\page.info", 'w', encoding="utf-8") as f:
                    f.write(str(CHAPTER_ID_1))

                txtArr = txtLine.split("、")
                txtLine = "\n第{0}章 {1}\n".format(CHAPTER_ID_1, txtArr[1])

            print(txtLine)
            write_txt_content(txtFileName, chapterName, txtLine)

    except Exception as e:
        time.sleep(2)
        print(chapterHtml)
        print(e)


def write_txt_content(txtFileName, chapterName, chapterTxt):
    with open(txtFileName, 'a', encoding="utf-8") as f:
        f.write(chapterTxt + "\n")

def get_html_all_content(url):
    # time.sleep(2)
    getFlag = False
    while getFlag == False:
        try:
            driver.get(url)
            html = driver.page_source

            if INDEX_DOWN_FLAG in html:
                getFlag = True
            elif SUB_DOWN_FLAG not in html:
                getFlag = False
                raise Exception("页面内容获取失败！！")
            else:
                getFlag = True

        except Exception as e:
            print(url, e)
            getFlag = False
            time.sleep(5)
    return html


if __name__ == '__main__':

    html = get_html_all_content(ROOT_URL)

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if os.path.exists(novelFilePath):
        os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:
        # print(chapterInfo)

        chapterUrl = "{0}{1}".format("https://www.mozhua.net/", chapterInfo["href"])

        chapterHtml = get_html_all_content(chapterUrl)

        chapterTxt = rtn_chapter_txt(chapterHtml, novelFilePath, chapterInfo["text"])

        print("路径：{0}，网址：{2}，正在获取 章节：{1} ！！！".format(chapterUrl, novelFilePath, chapterInfo["text"]))

        # write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt)
