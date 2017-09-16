#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import glob
import re
import os

path = r"C:\Users\steve\workspace\big_promotion.csv"

# merge data


def merge_excel(path, on=None):
    if os.path.isdir(path):
        all_data = pd.DataFrame()
        for f in glob.glob(path):
            df = pd.read_excel(f)
            df['store'] = f.split('/')[-1][:2]
            all_data = all_data.append(df, ignore_index=True)
    else:
        all_data = pd.read_csv(path, encoding='gb2312')
    cols = ['oid', 'order_status', 'seller',
            'buyer', 'email', 'bid_time', 'pay_time', 'amount',
            'freight', 'total', 'discount', 'product', 'remark',
            'address', 'reciever', 'country', 'state', 'city',
            'street', 'zip', 'phone', 'cell', 'choice', 'store']
    #
    all_data.columns = cols
    all_data['oid'] = all_data['oid'].astype('str')
    all_data['bid_time'] = pd.to_datetime(all_data['bid_time'])
    all_data['pay_time'] = pd.to_datetime(all_data['pay_time'])
    if on is not None:
        return all_data.drop_duplicates(on)
    else:
        return all_data

df = merge_excel(path, 'oid')
product_info = {}
for info in df['product']:
    if len(info) > 1:
        for detail in info:
            if detail[-2] in product_info:
                product_info[detail[-2]] += int(detail[-1])
            else:
                product_info[detail[-2]] = int(detail[-1])
    else:
        if info[0][-2] in product_info:
            product_info[info[0][-2]] += int(info[0][-1])
        else:
            product_info[info[0][-2]] = int(info[0][-1])

# remove '( )'


def bracrepl(matchobj):
    if matchobj.group(0) == '(' or matchobj.group(0) == ')':
        return ''

product_list = []


def tidy_product(df):
    for info in df['product']:
        product_info = {}
        if len(info) > 1:
            for detail in info:
                product_info['bid_time'] = df[
                    df['product'] == info]['bid_time']
                product_info['SKU'] = detail[-2]
                product_info['num'] = detail[-1]
                product_list.append(product_info)
        else:
            product_info['bid_time'] = df[df['product'] == info]['bid_time']
            product_info['SKU'] = info[0][-2]
            product_info['num'] = info[0][-1]
            product_list.append(product_info)
# Binning:


def binning(col, cut_points, labels=None):
    # Define min and max values:
    minval = col.min()
    maxval = col.max()

    # create list by adding min and max to cut_points
    break_points = [minval] + cut_points + [maxval]

    # if no labels provided, use default labels 0 ... (n-1)
    if not labels:
        labels = range(len(cut_points) + 1)

    # Binning using cut function of pandas
    colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
    return colBin

# Binning age:
cut_points = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60]
df['colprice'] = binning(df['total'], cut_points)
pd.value_counts(df['colprice'], sort=False)

# clean product


def tidy(x):
    temp = re.sub('[(|)]', bracrepl, x)
    if '产品属性' in temp:
        return re.findall(u'产品属性:(.*)\n商家编码:(.*)\n产品数量:(\d+)', temp)
    else:
        return re.findall(u'商家编码:(.*)\n产品数量:(\d+)', temp)
# 读入数据
df = pd.read_csv(path)
# print(df.head())
# gourp


def group(df, by='store', drop=[]):
    if drop == []:
        return df.groupby(by).sum()
    else:
        return df.dropna(subset=drop).groupby(['store']).sum()


cols = ['oid', 'pay_time', 'amount',
        'freight', 'total', 'store']

df = df.sort_values(by='bid_time')
df_paid = df[df['pay_time'].notnull()]
df_paid = df_paid.set_index('bid_time')
paid_amount_by_time = df_paid.resample('H').sum()
last = paid_amount_by_time[['total']]
last.columns = ['total_paid']
print(last)
# print(df.index)
df2 = df.set_index('bid_time')
amount_by_time = df2.resample('H').sum()
order_by_time = df2.resample('H').count()
right = amount_by_time[['total']]
right.columns = ['total_order']
print(right)
#order_by_time['pay_rate'] = order_by_time['pay_time']/order_by_time['oid']
#order_by_time['pay_rate'] = order_by_time['pay_rate'].map(lambda x: "{:.2%}".format(x))
#order_by_time['amount'] = amount_by_time['total']
#left = order_by_time[['oid','pay_time','pay_rate']]
# print(left)
#total = pd.concat([left,right, last], axis=1)
# print(total)
# total.to_csv('/home/steven/Documents/total_amount_by_time.csv')
# group by country

#print("bid amount:")
#store_df = group(df)
# print(store_df)
# print(store_df.sum())
#print("paid amount:")
#store_df = group(df, 'store', ['pay_time'])
# print(store_df)
# print(store_df.sum())
#order_status_df = group(df, 'order_status')
# print(order_status_df)
