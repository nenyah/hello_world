# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:12:53 2017

@author: steve
"""

import os
import pandas as pd

os.chdir('f:/workspace')


def tidy(url):    
    if '1688' in url:        
        url = url.split("?")[0]    
    elif 'tmall' in url or 'taobao' in url:        
        root,pendix = url.split("?")        
        url = root+"?"+pendix.split("&")[1]    
    return url

file = "在售产品信息.csv"
df = pd.read_csv(file, encoding='gbk')
