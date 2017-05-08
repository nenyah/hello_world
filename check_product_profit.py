# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:48:35 2017

@author: steve
"""

import pandas as pd
import numpy as np

file = r"C:\Users\steve\Desktop\product_profit.xls"

df = pd.read_excel(file)

single_df = df[~(df['SKU列表'].str.contains('<br'))]

print(len(df),len(single_df))

single_df['SKU'] = single_df['SKU列表'].map(lambda x: x.split('*')[0][:7])
single_df['销量'] = single_df['SKU列表'].map(lambda x: x.split('*')[-1])

#print(single_df.head())
single_df['订单编号'] = single_df['订单编号'].astype('object')
single_df = single_df.dropna(axis=0)
profit = single_df.groupby(by='SKU').sum().sort('实际毛利润')
print(profit)
profit.to_excel('12月产品利润表.xlsx')