#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
Tidy Bookmarks
Version:    2016-09-20
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import requests
from bs4 import BeautifulSoup
from Tool.tool import get_filenames
import pandas as pd


# 收藏夹导出的本地文件， html格式
path = r"E:\Work\wwwroot\Code\bookmark"


def get_bookmarks(path):
    # 读取并编码
    with open(path, encoding='utf-8') as html:
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(html, 'lxml')
        # 定义字典用来存取内容
    bookmarks = []
    # 查找内容， 因为收藏夹内有整理把相关内容收进一个文件夹
    for info in soup.select('dl dt'):
        # 存取查找内容
        data = {}
        try:
            # h3是文件夹名
            h3 = info.find_all('h3')
            if h3:
                data['file'] = h3[0].text
            # a是收藏的网页
            a = info.find_all('a')
            if a:
                # 获取网页的地址和名称
                data['link'] = a[0]['href']
                data['name'] = a[0].text
        except TypeError:
            pass
        # print(data)
        bookmarks.append(data)
    print('Total:', len(bookmarks))
    return bookmarks
files = get_filenames(path)
bookmarks = []
for file in files:
    for info in get_bookmarks(file):
        if info not in bookmarks:
            bookmarks.append(info)
        else:
            # print(info,'Repeate')
            pass
print('#' * 50)
print(len(bookmarks))
df = pd.DataFrame(bookmarks)
print(df.head())
df.to_csv('bookmarks.csv', index=False)
