#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
合并目录下的所有excel文件，去重后存入新的excel
Version:    2016-10-10
Author:     Steven
Contact:    lucibriel (at) 163.com
"""

import os
import glob
import pandas as pd


def merge_excel(path, on='ERP订单号'):
	"""合并数据"""
	all_data = pd.DataFrame()
	for f in glob.glob(path):
		df = pd.read_excel(f)
		all_data = all_data.append(df, ignore_index=True)
	return all_data.drop_duplicates(on)


if __name__ == '__main__':
	print('Program is running...')
	path = r'E:\Work\06-Work\00-Todo\Self Calc\Freight Self Calc Download\*'
	target_path = r'E:\Work\06-Work\00-Todo\Self Calc\Freight Self Calc Sort'

	df = merge_excel(path)
	df.to_excel(os.path.join(target_path,"Total.xlsx"),index=False)
	print('Success!')