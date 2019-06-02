# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/17 8:43'

import time
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

# 单一小说网址
novelId = "29/29599"
ROOT_URL = "https://www.qisuu.la/du/{0}/".format(novelId)
DOWN_FLODERS = r"E:\下载小说"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
headers = {'Host': ROOT_URL}
headers = {'Referer': ROOT_URL}
headers = {'Upgrade-Insecure-Requests': '1'}


def rtn_chapter_list_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"class": "info_des"})[0].h1.text
    print(novelName)

    chapterListInfoSoup = soup.find_all(name="div", attrs={"id": "info"})[2].find_all(name="li")

    chapterListInfoArr = []

    for ddItem in chapterListInfoSoup:

        chapterListInfoDict = OrderedDict()

        if "href" not in str(ddItem):
            continue

        chapterListInfoDict["text"] = ddItem.a.text
        chapterListInfoDict["href"] = ddItem.a["href"]
        # print(chapterListInfoDict)

        chapterListInfoArr.append(chapterListInfoDict)

    return chapterListInfoArr, novelName


def rtn_chapter_txt(chapterHtml):
    soup = BeautifulSoup(chapterHtml, 'html.parser')

    # print(chapterHtml)

    txtContent = soup.find_all(name="div", attrs={"id": "content1"})[0].text

    txtContent = txtContent.replace("一秒记住【顶点小说网 www.23wx.so】，精彩小说无弹窗免费阅读！", "")
    txtContent = txtContent.replace("       ", "")
    txtContent = txtContent.replace("        ", "")
    txtContent = txtContent.replace("    ", "")
    txtContent = txtContent.replace(" ", "")
    txtContent = txtContent.replace("～", "")
    txtContent = txtContent.replace("\r\n", "")
    txtContent = txtContent.replace("\n\n", "")
    # txtContent = txtContent.replace('\xa0','')
    # txtContent = txtContent.replace('\ue4c6','')
    # txtContent = txtContent.replace('\ue0d8','')

    return txtContent


def write_txt_content(txtFileName, chapterName, chapterTxt):
    with open(txtFileName, 'a', encoding="utf-8") as f:
        # f.write(chapterName + "\n")
        f.write(chapterTxt + "\n\n")


def get_html_all_content(url):
    getFlag = False
    while getFlag == False:
        try:
            html = requests.get(url=url, params=headers)
            html = html.content.decode('utf-8', 'ignore')
            getFlag = True
        except Exception as e:
            print(url, e)
            getFlag = False
            time.sleep(5)
    return html


if __name__ == '__main__':

    html = get_html_all_content(ROOT_URL)
    # print(ROOT_URL)

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if os.path.exists(novelFilePath):
        os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:
        # print(chapterInfo)

        chapterUrl = "{0}/{1}".format(ROOT_URL, chapterInfo["href"])

        chapterHtml = get_html_all_content(chapterUrl)

        chapterTxt = rtn_chapter_txt(chapterHtml)

        print("路径：{0}，正在获取 章节：{1} ！！！".format(novelFilePath, chapterInfo["text"]))

        write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt)
