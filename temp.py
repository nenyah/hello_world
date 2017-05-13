#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

from cal_eub_freight import calc_eub
import pandas as pd
import os

os.chdir(r"F:\workspace")
path = r"F:\workspace\Epacket.xls"
df = pd.read_excel(path)
freight = []
for track in df['快递单号']:
    is_track = df['快递单号'] == track
    country = df[is_track]['国家'].values[0].lower()
    weight = df[is_track]['称重重量'].values[0]
    try:
        cost = calc_eub(country, weight)
        print(cost)
        freight.append(cost)
    except:
        print(track)
print(freight)
df['结算运费'] = pd.Series(freight)
df = df.loc[:, ['快递单号', '称重重量', '结算运费']]
df.columns = ['物流单号', '结算重量', '结算运费']
df.to_csv("计算结果.csv", index=False)
df.to_clipboard(index=False)
