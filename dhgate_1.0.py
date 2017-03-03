#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
通过关键词，获取指定页数的产品相关信息
	产品标题，产品价格，产品销量
Version:    2017-03-03
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re

key_word = 'women shoes'

url = 'http://www.dhgate.com/w/{}/{}.html'.format(quote_plus(key_word),str(1))
print(url)
headers = {
	'User_Agents': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
}
# url = 'http://www.dhgate.com/w/women+shoes/1.html'
r = requests.get(url, headers=headers)
# print(r.encoding)
r.encoding = 'utf-8'
print(r.text)
# r.encoding = 'utf-8'
# soup = BeautifulSoup(r.text, 'lxml')
# print(soup)


