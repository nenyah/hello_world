#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
测试Demo
Version:    2016-07-27
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import requests
from bs4 import BeautifulSoup

url = 'http://www.23wx.com/html/52/52855/'

r = requests.get(url)
print(r.encoding)
r.encoding='gbk'
soup = BeautifulSoup(r.text,'lxml')
links = soup.select('tbody td')

print(links)
