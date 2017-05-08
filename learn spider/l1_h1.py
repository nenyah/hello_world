#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import requests
import time

def gethtml(url):
	try:
		r = requests.get(url)
		r.raise_for_status
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "something wrong"

if __name__ == '__main__':
	start = time.time()
	url = 'http://www.baidu.com'
	for i in range(100):
		gethtml(url)
		print('Get baidu {0} times'.format(i+1))
	end = time.time()
	print('100 times use: {0}'.format(end-start))