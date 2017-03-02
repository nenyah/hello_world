#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
按SKU批量指定采购价
Version:    2016-08-24
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import re
import xlrd

def save_sku_price(source_path,target_path,A_PRICE = 8.58,E_PRICE = 17.48):
	# 读取xls数据
	sheet = xlrd.open_workbook(source_path).sheet_by_index(0) #读取sheet1
	sku_from_exl = [] #存储exl中读出的sku
	for i in range(sheet.nrows):
		sku_from_exl.append(sheet.cell_value(i,5))
	# 存储数据用
	sku_list = []

	# SKU格式
	pattern_e = r'E\w{1,3}$'
	pattern_a = r'A\w{1,3}$'

	# 把数据存入列表
	for item in sku_from_exl:
		data = {}
		if re.search(pattern_a,item):
			data = {
			'sku': item,
			'price': A_PRICE
			}
		elif re.search(pattern_e,item):
			data = {
			'sku': item,
			'price': E_PRICE
			}
		else:
			print(item)
			continue
		sku_list.append(data)

	# 写入文件
	with open(target_path,'a+') as f:
		f.write('产品SKU,实际采购成本\n')
		for item in sku_list:
			# print(item)
			print(item['sku'],item['price'])
			f.write('{},{}\n'.format(item['sku'],item['price']))

if __name__ == '__main__':
	source_path = r'C:\Users\steve\Desktop\EATGE_price.xls'
	target_path = r'C:\Users\steve\Desktop\sku.csv'
	save_sku_price(source_path,target_path)