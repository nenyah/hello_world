#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Steven Tan'

import requests
from bs4 import BeautifulSoup

page = 4

data = {
	'marketplaceID':'ATVPDKIKX0DER',
	'seller':'A294P4X9EWVXLJ',
	'pageNumber':page
	}

url = 'https://www.amazon.com/sp/ajax/products'
session = requests.Session()
wb_data = session.post(url,data=data)
js = wb_data.json()
for item in js['products']:
	for k,v in item.items():
		print('{0} => {1}'.format(k,v))
	print('='*60)	
