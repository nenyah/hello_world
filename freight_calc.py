#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
compute freight refactor price_calc_out.py
Version:    2016-09-18
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import os
import pandas as pd

# global discount dict
DISCOUNT = {
	'cn_post': 0.82,
	'ru_express': 0.72,
	'electric': 0.77
	}

def get_ref(path = r'freight_standard.xls'):
	"""read the ref data
	Keyword arguments: 
	----------------------
	path default(freight_standard.xls)
	Returns: DataFrame
	"""
	xlsx = pd.ExcelFile(path)
	df = pd.read_excel(xlsx, 'register')
	df = df.loc[:,['英文','资费标准（元/kg)']]
	df.columns = ['country','price']
	return df

df = get_ref()

def get_price(country):
	"""get the standard price form country
	Parameters
	----------
	country: str

	Retruns
	-------
	price
	"""
	return df[df['country'] == country].price.values[0]

def calc_eub(country,weight):
	if country.strip() == 'United States':
		try:
			if weight < 70:
				result = 14.6
			elif weight <= 200:
				result = weight*0.08 + 9
			elif weight < 2000:
				result = weight*0.075 + 9
			print(weight,result)

		except TypeError:
			print('EUB weight is empty')
	elif country.strip() == 'Russian Federation':
		result = weight*0.08 + 8
	else:
		result = weight*0.07 + 22
	return round(result,2)

def calc(country,weight,freight):
	"""calc the price form parameters
	Parameters
	----------
	country: str country value
	weight: float weight value
	freight: str freight value

	Returns
	-------
	float the price of the calc result
	"""
	result = 0
	if '小包' in freight:
		freight = 'cn_post'
	elif '专线' in freight:
		freight = 'ru_express'
	elif '宝' in freight:
		freight = 'eub'
	elif '苍南' or '昆山' in freight:
		freight = 'electric'

	if freight in ['cn_post','ru_express','electric']:
		try:
			result = (get_price(country)*10**-3*weight+8)*DISCOUNT[freight]
		except TypeError:
			print('CN_POST weight is empty')
	elif freight == 'eub':
		result = calc_eub(country,weight)
	return round(result,2)


def save_excel(source_path,target_path=None):
	"""compute data from source file and generate a new file
	Parameters
	----------
	source_path: file
	target_path: file
	"""
	print('Begin...')
	if target_path == None:
		target_path = os.path.splitext(source_path)[0]+'_res.csv'
	df = pd.read_csv(source_path, encoding='gb2312')
	df = df.dropna(subset=['快递单号'])
	freight = []
	for track in df['快递单号']:
		is_track = df['快递单号'] == track
		country = df[is_track]['国家'].values[0]
		weight = df[is_track]['实际重量(g)'].values[0]
		channel = df[is_track]['发货渠道'].values[0]
		try:
			freight.append(calc(country, weight, channel))
		except:
			print(track)

	df['结算运费'] = pd.Series(freight)
	new_df = df.loc[:,['发货渠道','国家','快递单号','实际重量(g)','结算运费']]
	new_df.columns = ['发货渠道','国家','物流单号','结算重量','结算运费']
	new_df.to_csv(target_path, index=False)
	print('Done!')


if __name__ == '__main__':
	path = r'E:\Work\06-Work\00-Todo\Self Calc\Freight Self Calc Sort\Total.csv'
	save_excel(path)