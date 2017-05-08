#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
from crawler_tool import requests
import time,re
from bs4 import BeautifulSoup

paths = [r"https://naturalhome.aliexpress.com/store/518251/search/{0}.html".format(str(i)) for i in range(1,11)]

def getDiscount(path):
	try:
		reps = requests.get(path)
		soup = BeautifulSoup(reps.text,'lxml')
		item = soup.find_all('li',class_="item")
		for info in item:
			p_url = info.h3.a.get("href")
			pid = p_url.split("_")[-1].split(".")[0]
			discount = info.find(class_="discount").text.strip() if info.find(class_="discount") else None
			print(pid,discount)
			with open("discount.txt","a") as f:
				f.write("{0},{1}\n".format(pid,discount))
	except Exception as e:
		raise e

for path in paths:
	getDiscount(path)