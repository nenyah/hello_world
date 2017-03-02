#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
获取指定地址文章
Version:    2016-09-03
Author:     Steven
Contact:    lucibriel (at) 163.com
"""

import requests
from bs4 import BeautifulSoup

# 从列表页取得内容页链接
def get_link(url):
	header = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	}
	site = 'http://www.chinasalestore.com'
	web_data = requests.get(url,headers=header)
	soup = BeautifulSoup(web_data.text,'lxml')
	urls = soup.select('h3 a')
	content_urls = []
	for url in urls:
		if '亚马逊日销1000刀运营日志' in url.text:
			content_urls.append(site+url.get('href'))
	return content_urls

# 从内容页取得内容	
def get_content(url):
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text,'lxml')
	# print(soup)
	contents = soup.select('.arc-con-article')
	content_list = []
	for content in contents:
		text = content.text.replace('\n','')
		print(text,end='\n')
		print()
		if '\n' not in text:
			content_list.append(text)
	# print(content_list)
	# for content in content_list:
	# 	print(content)
	return content

# 列表地址
url = 'http://www.chinasalestore.com/index.php/index/toutiao.html?&p='
list_url = [url+'{}'.format(str(i)) for i in range(9,49)]
print(list_url[0])
# 测试
url = get_link(list_url[23])[0]
print(url)
get_content(url)