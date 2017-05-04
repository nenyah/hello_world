#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
from exceltool import makePath
import pandas as pd
import os,re




# 读入路径，添加pid列
def get_df(path):
	if os.path.splitext(path)[-1] == ".xls":
		df = pd.read_excel(path)
		pid = os.path.split(path)[-1]
		_,pid,_ = re.split(r"[_|.]", pid)
		df['pid'] = pid
		return df

# 存储数据
def save(paths, file):
	print("开始分析数据")
	data = list(map(get_df, paths))
	df = pd.concat(data)
	df.to_csv(file,index=False)
	print("保存成功！")

#

if __name__ == '__main__':
	root = r"E:\Work\06-Work\Data Anlysis\03-商品数据\2017\Mon3"
	file = r"E:\Work\06-Work\Data Anlysis\03-商品数据\2017\汇总\total.csv"
	df = pd.read_csv(file, encoding="gbk")
	df_sort = df[df['国家'] == '全球']
	print(len(df))
	print(len(df_sort))
