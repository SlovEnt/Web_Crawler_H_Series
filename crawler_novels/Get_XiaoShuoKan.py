# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/18 12:39'

import time
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from global_function import get_html_all_content, chrome_get_html_all_content

# 未完成！！！！！！

# 单一小说网址
novelId = "28386"
ROOT_URL = "https://www.xiaoshuokan.com/haokan/{0}/index.html".format(novelId)
DOWN_FLODERS = r"E:\下载小说"

def rtn_chapter_list_info(html):

    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"class": "booktitle"})[0].h1.text
    novelName = novelName.replace("（完）全文阅读", "")
    novelName = novelName.strip()
    novelName = novelName.split("作者")[0]
    print(novelName)

    chapterListInfoSoup = soup.find_all(name="span", attrs={"class": "c1"})

    chapterListInfoArr = []

    for ddItem in chapterListInfoSoup:

        chapterListInfoDict = OrderedDict()

        if "href" not in str(ddItem):
            continue

        chapterListInfoDict["text"] = ddItem.a.text
        chapterListInfoDict["href"] = ddItem.a["href"]
        print(chapterListInfoDict)

        chapterListInfoArr.append(chapterListInfoDict)

    return chapterListInfoArr, novelName


def rtn_chapter_txt(chapterHtml):
    # html = str(chapterHtml)
    # chapterHtmlReg = re.compile(r"(<a href=\"/xiaoshuo/.+?\n.+?\n.+?\n.+?\n.+?</script>)", re.M)
    # chapterHtml2 = chapterHtmlReg.findall(html)[0]

    # print(chapterHtml2)

    # chapterHtml = html.replace(chapterHtml2, "")

    soup = BeautifulSoup(chapterHtml, 'html.parser')

    txtContent = soup.find_all(name="class", attrs={"class": "bookcontent"})[0].text

    # txtContent = str(txtContent).replace("<br/>", "\n")

    print(txtContent)
    # time.sleep(2000)

    # txtContent = BeautifulSoup(txtContent, 'html.parser').text


    txtContent = txtContent.replace('　　', '')
    txtContent = txtContent.replace('\n\n', '\n')
    # txtContent = txtContent.replace('\ue4c6','')
    # txtContent = txtContent.replace('\ue0d8','')
    # print(txtContent)

    return txtContent


def write_txt_content(txtFileName, chapterName, chapterTxt):
    with open(txtFileName, 'a', encoding="UTF-8") as f:
        f.write(chapterName + "\n")
        f.write(chapterTxt + "\n\n")

if __name__ == '__main__':

    html = chrome_get_html_all_content(ROOT_URL, "booktitle")

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if os.path.exists(novelFilePath):
        os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:
        # print(chapterInfo)

        chapterUrl = "{0}{1}".format("https://www.xiaoshuokan.com", chapterInfo["href"])
        print(chapterUrl)

        chapterHtml = chrome_get_html_all_content(chapterUrl, "content")
        chapterTxt = rtn_chapter_txt(chapterHtml)
        print(chapterTxt)

        print("路径：{0}，正在获取 章节：{1} ！！！".format(novelFilePath, chapterInfo["text"]))

        write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt)
