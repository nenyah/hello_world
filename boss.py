#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import requests
import lxml
from bs4 import BeautifulSoup

path = r"http://www.zhipin.com/job_detail/?query=Python&scity=101210400&source=2"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Host': 'www.zhipin.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
}

resp = requests.get(path, headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')

b = soup.select("span.red")
[print(c.get_text()) for c in b]
