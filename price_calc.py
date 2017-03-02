#! /usr/bin/env python3.5
# coding:utf-8
import xlrd
from xlwt import *

'''
@name: price_calc.py
@author:steven
@date: 2016-05-13
@des: 用于各种渠道运费计算
'''
def get_ref():
	# 读入参考excel
	path = r'freight_standard.xls'
	wb = xlrd.open_workbook(path)
	sheet = wb.sheet_by_name('register')
	nrows = sheet.nrows
	ref = []
	for i in range(1, nrows):
		if sheet.cell_value(i,2) != 42:
			data = {
			'country': sheet.cell_value(i,2),
			'price': sheet.cell_value(i,4)
			}
			ref.append(data)
	return ref
# 一次性加入内存，减少读入次数
ref = get_ref()


# 按规则计算得到运算结果
def calc(country,weight,freight):
	'''
	@country: 国家
	@weight: 重量
	@freight: 渠道
	'''
	result = 0
	if '小包' or 'CORREOS' in freight:
		freight = 'cn_post'
	elif '专线' in freight:
		freight = 'ru_express'
	elif '宝' in freight:
		freight = 'eub'
	elif '苍南' or '昆山' in freight:
		freight = 'electric'
	# print(freight)
	discount = {
	'cn_post': 0.82,
	'ru_express': 0.72,
	'electric': 1
	}

	if freight in ['cn_post','ru_express','electric']:
		for item in ref:
			if country == item['country']:
				try:
					result = (item['price']*10**-3*weight+8)*discount[freight]
				except TypeError:
					print('CN_POST weight is empty')
	elif freight == 'eub':
		try:
			if weight < 70:
				result = 70 * 0.08 + 9
			elif weight <= 200:
				result = weight * 0.08 + 9
			elif weight < 2000:
				result = weight * 0.075 + 9
			# print(weight,result)
		except TypeError:
			print('EUB weight is empty')
	else:
		pass
	return round(result,2)


def save_excel(source_path,target_path,sheet_name='calc freight',):
	# 读入excel
	# 路径
	source_path = source_path
	# 打开excel
	wb = xlrd.open_workbook(source_path)
	# 打开sheet1
	sheet = wb.sheet_by_index(0)
	# 读入行数
	nrows = sheet.nrows

	# 写excel
	w = Workbook(encoding='utf-8')
	# 添加sheet calc freight
	ws = w.add_sheet(sheet_name)
	# 写标题
	counter = 1
	titles = ['渠道','国家','物流单号','结算重量','结算运费']
	for index,item in enumerate(titles):
		ws.write(0,index,item)
	# 写内容
	for i in range(1, nrows):
		freight = sheet.cell_value(i,5)
		track = sheet.cell_value(i,6)
		weight = sheet.cell_value(i,7)
		country = sheet.cell_value(i,16)
		result = calc(country,weight,freight)
		data = [freight,country,track,weight,result]
		for index, item in enumerate(data):
			ws.write(counter,index,item)
		counter += 1

	# 存储excel
	w.save(target_path)

if __name__ == '__main__':
	path = r'freight_calc_20160516.xls'
	save_excel(path,'test_1.xls')