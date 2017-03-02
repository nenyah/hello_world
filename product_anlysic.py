#! /usr/bin/env python3
# coding:utf-8
"""
@auth:Steven
@date:2016-08-09
func: 产品盈亏分析
"""
import pandas as pd
import os

def read_data(file):
	"""按照不同格式，读入数据"""
	sufix = os.path.splitext(file)[-1]
	if sufix in ['.xls','.xlsx']:
		df = pd.read_excel(file,index_col=None, headers = 0, na_values=['NA'])
	elif sufix in ['.txt','.csv']:
		df = pd.read_csv(file,sep='\t', header=0, dtype=str, na_filter=False)
	df['实际毛利润'] = df['实际毛利润'][df['实际毛利润'] != ''].astype(float)
	df["SKU列表"] = df["SKU列表"].astype(str)
	# print(df.dtypes)
	return df

def get_single(data):
	"""获取单款单订单内容"""
	df = data
	df["SKU"] = [str(data).split('<br/>') for data in df["SKU列表"]]
	df1 = df[df["SKU"].map(lambda x: len(x) == 1)]
	df1['SKU_'] = [data[0].split('*')[0] for data in df1['SKU']]
	df1['Order'] = [data[0].split('*')[-1] for data in df1['SKU']]
	print(df1.head())
	# print(df.describe())


def get_multi(data):
	"""获取多款单订单内容"""
	pass

if __name__ == '__main__':
	file = r'E:\Work\06-Work\01-数据分析\12-盈亏分析\Mon7B_PA\Mon7_product.txt'
	data = read_data(file)
	get_single(data)