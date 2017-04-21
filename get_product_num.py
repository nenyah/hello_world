#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
# 导入所需库
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

def getProductNum(el):
    time.sleep(3)
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    try:
        reps = requests.get(el,headers=headers).text
        soup = BeautifulSoup(reps,'lxml')
        num = soup.select("#result-info")[0].text.strip("\n").split(" ")[0]
        print(num)
        # num = int(re.findall(r'\d+,?\d+', num)[0])
        return num
    except:
        return 'null'

path = r"https://cyclingjerseystore.aliexpress.com/store/all-wholesale-products/1079069.html"

print(getProductNum(path))