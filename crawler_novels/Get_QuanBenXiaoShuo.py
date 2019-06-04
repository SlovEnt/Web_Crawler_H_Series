# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/11 9:26'

'''
https://www.rourouwu.com/read
'''

import time
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from global_function import get_html_all_content, chrome_get_html_all_content


novelId = "37815"  #
ROOT_URL = "https://www.rourouwu.com/read/{0}/".format(novelId)
DOWN_FLODERS = r"E:\下载小说"

# 页面获取判断标志 正常html页面里的唯标识
INDEX_DOWN_FLAG = "infotitle"
SUB_DOWN_FLAG = "srcbox"

def rtn_chapter_list_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"class": "infotitle"})[0].h1.text
    print("开始下载《{0}》".format(novelName))

    chapterListInfoSoup = soup.find_all(name="div", attrs={"id": "box"})[0].find_all(name="dd")

    for x in chapterListInfoSoup:
        print(str(x))

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

    try:
        txtContent = soup.find_all(name="div", attrs={"id": SUB_DOWN_FLAG})[0].text
    except:
        time.sleep(2)
        print(chapterHtml)

    txtContent = txtContent.split("最新章节！")[1]

    txtContent = txtContent.replace("一秒记住【顶点小说网 www.23wx.so】，精彩小说无弹窗免费阅读！", "")
    txtContent = txtContent.replace("       ", "")
    txtContent = txtContent.replace("        ", "")
    txtContent = txtContent.replace("    ", "")
    txtContent = txtContent.replace(" ", "")
    txtContent = txtContent.replace("～", "")
    txtContent = txtContent.replace("\r\n", "")
    txtContent = txtContent.replace("\n\n", "")
    txtContent = txtContent.replace('\xa0', '')
    txtContent = txtContent.replace('ůɼɛొ节Ŕ!Eŋ百ƮnΦΩߍᢢ', '')
    txtContent = txtContent.replace('ůɼɛొ节Ŕ!Eŋ百ƮnΦΩߍᢢ 的	F/Ɖ', '')
    txtContent = txtContent.replace('更多精品女生婚恋小说，请·百度·或·360·上搜索：我\/的\书\/城\/网', '')
    txtContent = txtContent.replace('二五八中雯.2.5.8ｚw.cōm', '')
    txtContent = txtContent.replace('②miào②bi.*②阁②，', '')
    txtContent = txtContent.replace('ｈttp：／／ｗww．ｂａnfｕ.*ｓheｎｇ．ｃｏｍ', '')
    txtContent = txtContent.replace('⑧☆miào⑧☆bi(.*)gé⑧☆.＄.', '')
    txtContent = txtContent.replace('△miào△bi△gé△', '')
    txtContent = txtContent.replace('二五八中雯', '')
    txtContent = txtContent.replace('贰伍捌中文', '')
    txtContent = txtContent.replace('贰伍捌中文wｗw.⒉58zw.cōm最快更新', '')
    txtContent = txtContent.replace('二五八中雯.2.5.8ｚw.cōm', '')
    txtContent = txtContent.replace('[$妙][笔$i][-阁].', '')
    txtContent = txtContent.replace('贰伍捌中文.⒉58zw.cōm', '')
    txtContent = txtContent.replace('258中文阅读网', '')
    txtContent = txtContent.replace('】⑨八】⑨八】⑨读】⑨书，.2≧3.o↗贰伍捌中文', '')
    txtContent = txtContent.replace('误嫁天价老公最新章节『我』『的』『书』『城』『网』『首』『发』', '')

    txtContent = txtContent.replace('\u016f', '')
    txtContent = txtContent.replace('\u027c', '')
    txtContent = txtContent.replace('\u025b', '')
    txtContent = txtContent.replace('\u0c4a', '')
    txtContent = txtContent.replace('\u0154', '')
    txtContent = txtContent.replace('\u0189', '')
    return txtContent

def write_txt_content(txtFileName, chapterName, chapterTxt):
    with open(txtFileName, 'a') as f:
        f.write(chapterName + "\n")
        f.write(chapterTxt + "\n\n")


if __name__ == '__main__':

    html = get_html_all_content(ROOT_URL, "infotitle", "gbk")

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if os.path.exists(novelFilePath):
        os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:
        # print(chapterInfo)

        chapterUrl = "{0}{1}".format(ROOT_URL, chapterInfo["href"])

        chapterHtml = get_html_all_content(chapterUrl)

        chapterTxt = rtn_chapter_txt(chapterHtml)

        print("路径：{0}，网址：{2}，正在获取 章节：{1} ！！！".format(chapterUrl, novelFilePath, chapterInfo["text"]))

        write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt)
