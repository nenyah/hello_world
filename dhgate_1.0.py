#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
通过关键词，获取指定页数的产品价格与销售数量
Version:    2017-04-09
Author:     Steven
Contact:    lucibriel (at) 163.com
modify:     重构dhgate.py
file:       dhgate_1.0.py
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus
import sys
from numpy import mean

def buildUrl(keyword="women shoes", page=1):
	key_word = quote_plus(keyword)
	urls = ['http://www.dhgate.com/w/{}/{}.html'.format(key_word,str(i)) for i in range(page)]
	return urls


def getData(url, data=None):
	data = []
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text,'lxml')


	items = soup.find_all("div", "listitem")
	for item in items:
		title = item.find("h3").find("a").text # 标题
		price = item.find("li","price").text #价格
		m = re.findall(r'(\d+\.*\d+)', price)
		price = mean(list(map(float, m))) # 计算均价
		attribute = item.find("ul", "attribute").text
		min_order = re.findall(r'Min. Order: (\d+)', attribute)[0] #起订量
		order = re.findall(r'Sold: (\d+)', attribute)
		order = order[0] if len(order) > 0 else 0 #订单量
		feedback = item.find("span","reviewnum")
		feedback = re.findall(r"\d+", feedback.text)[0] if feedback else 0
		seller = list(item.find("span","seller").stripped_strings)[-1]
		store_url = item.find("span","seller").find("a")['href']
		store_feedback = item.find("li","feedback")
		store_feedback = re.findall(r"\d+\.*\d+", store_feedback.text)[0] if store_feedback else 0
		info = {
			'title': title,
			'price': price,
			'min_order': min_order,
			'order': order,
			'feedback': feedback,
			'seller': seller,
			'store_url': store_url,
			'store_feedback': store_feedback
		}
		data.append(info)
	return data


def saveData(data, path='dhgate.csv'):
	print(data)
	# with open(path, 'a') as f:
	# 	f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format())

if __name__ == '__main__':
	urls = buildUrl()
	data = [getData(url) for url in urls]
	saveData(data)