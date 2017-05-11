#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

from freight_calc import calc_eub
import pandas as pd

path = r'C:\Users\steve\Desktop\运费计算.xls'
df = pd.read_excel(path)
freight = []
for track in df['快递单号']:
    is_track = df['快递单号'] == track
    country = df[is_track]['国家'].values[0]
    weight = df[is_track]['称重重量'].values[0]
    try:
        freight.append(calc_eub(country, weight))
    except:
        print(track)
print(freight)
df['结算运费'] = pd.Series(freight)
df.to_csv("计算结果.csv", index=False)
