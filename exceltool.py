#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import os

def checkSheet(xlsx):
	"""检查sheet数，返回数量"""
	return len(xlsx.sheet_names)


def isEqual(xlsx):
	"""检查多个sheet列是否相等"""
	df = dict()
	for name in xlsx.sheet_names:
		df[name] = pd.read_excel(xlsx, name)
		print(df[name].columns)
	num_of_columns = []
	for name in df.keys():
		num_of_columns.append(len(df[name].columns))
	for i in num_of_columns:
		if i != num_of_columns[0]:
			return False
	return True


path = r"E:\01-采购管理\采购表汇总\户外"

def makePath(path, files=None):
	files = []
	for i in os.walk(path):
		if i[2]:
			for name in i[2]:
				files.append(os.path.join(i[0],name))
	return files

files = makePath(path)
xlsx = pd.ExcelFile(files[0])
df = dict()
for name in xlsx.sheet_names:
	df[name] = pd.read_excel(xlsx, name)
print(df.keys())