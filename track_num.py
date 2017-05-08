#! /user/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Function:
跟踪号查询
Version:    2016-09-07
Author:     Steven
Contact:    lucibriel (at) 163.com
"""

import requests
from bs4 import BeautifulSoup

header = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

trackNum = 'RO312908771EE'

def get_track_info(trackNum):
	url = 'http://global.cainiao.com/detail.htm?mailNoList={0}'.format(trackNum)
	r = requests.get(url)
	print(r)
	soup = BeautifulSoup(r.text, 'lxml')
	result = soup.select('#waybill_path')
	print(result)

get_track_info(trackNum)