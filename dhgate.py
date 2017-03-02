#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
通过关键词，获取指定页数的产品价格与销售数量
Version:    2016-05-12
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus
import sys


def save_data(url,path='dhgate.csv',data=None):
	"""存储数据
	Parameter：
	url -- 爬取地址
	path -- 储存路径
	data -- 数据
	"""
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.text,'lxml')
	prices = []
	orders = []
	for item in soup.select('#proList .price'):
		m = re.search(r'(\d*.\d*) - (\d*.\d*)',item.text)
		if m:
			price = float(m.group(1))+float(m.group(2))
			prices.append(round(price/2,2))
		else:
			pass
	for item in soup.select('#proList .attribute'):
		m = re.search(r'Sold: (\d+)',item.text)
		if m:
			orders.append(m.group(1)) 
		else:
			orders.append(None)

	for price, order in zip(prices,orders):
		data = {
		'price': price,
		'order': order
		}
		print(data)
		with open(path,'a') as f:
			f.write('{},{}\n'.format(data['price'],data['order']))

def get_data(key_word,page_num):
	key_word = quote_plus(key_word)
	urls = ['http://www.dhgate.com/w/{}/{}.html'.format(key_word,str(i)) for i in range(page_num)]
	for url in urls:
		save_data(url,key_word+'.csv')

if __name__ == '__main__':
	key_word,page_num = sys.argv[1:3]
	get_data(key_word,int(page_num))