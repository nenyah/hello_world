# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-11-09 13:00:34
# @Last Modified by:   steven
# @Last Modified time: 2017-11-09 16:41:23
import requests
import os
import time

os.chdir(r'F:\f')
print(os.getcwd())


site = r"https://alcdn.hls.xiaoka.tv/20171027/c5a/812/RxFISGs6aTkIW6aX/"


def get_content(url):
    try:
        res = requests.get(url).content
    except:
        pass
    return res


def save(res, file):
    with open(file, "wb") as f:
        f.write(res)


def spider(init_page=0, last_page=738):
    for page in range(init_page, last_page):
        url = f"{site}{str(page)}.ts"
        print(url)
        res = get_content(url)
        time.sleep(3)
        page = "0" * (3 - len(str(page))) + str(page)
        save(res, page + ".ts")

if __name__ == '__main__':
    spider(8, 10)
