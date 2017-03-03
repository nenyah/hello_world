#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
通过关键词，获取指定页数的产品价格与销售数量
Version:    2017-03-03
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus
import sys
from numpy import mean


def save_data(url,path='dhgate.csv',data=None):
	"""存储数据
	Parameter：
	url -- 爬取地址
	path -- 储存路径
	data -- 数据
	"""
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
		data = {
			'title': title,
			'price': price,
			'min_order': min_order,
			'order': order,
			'feedback': feedback,
			'seller': seller,
			'store_url': store_url,
			'store_feedback': store_feedback
		}
		print(data)
		with open(path,'a') as f:
			f.write('{},{},{},{},{},{},{},{}\n'.format(
				data['title'],
				data['price'],
				data['min_order'],
				data['order'],
				data['feedback'],
				data['seller'],
				data['store_url'],
				data['store_feedback']
				))


def get_data(key_word,page_num):
	key_word = quote_plus(key_word)
	urls = ['http://www.dhgate.com/w/{}/{}.html'.format(key_word,str(i)) for i in range(page_num)]
	for url in urls:
		save_data(url,key_word+'.csv')

if __name__ == '__main__':
	key_word,page_num = sys.argv[1:3]
	get_data(key_word,int(page_num))