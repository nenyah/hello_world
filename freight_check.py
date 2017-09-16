#! /user/bin/env python3.5
# -*- coding: utf-8 -*-
"""
check carrier freight
version: 2016-09-12
Author: Steven
Contact: lucibriel(at)163.com
"""
import os
import pandas as pd
import re
import matplotlib.pylab as plt

# 获取货代数据


def get_carrier_data(path):
    # 表头
    cols = ['date', 'track_id', 'customer', 'desitnation', 'number',
            'weight', 'standard_price', 'discount', 'real_price',
            'channel']
    # 读取数据
    datas = pd.read_excel(path, sheetname=None)
    del_keys = [i for i in datas.keys() if not re.search(r'\d+\.\d+', i)]

    for i in del_keys:
        del datas[i]

    for i in datas.keys():
        datas[i] = datas[i].dropna(axis=0)
        datas[i].columns = cols

    # 汇总数据
    df = pd.concat([datas[i] for i in datas.keys()])
    df.weight = df.weight * 1000
    return df

# 获取ERP数据


def get_erp_data(path):
    df = pd.read_excel(path)
    cols = ['ERP_id', 'order_id', 'carrier', 'channel',
            'paid_time', 'delivery_time', 'track_id',
            'country_cn', 'country_en', 'weight_erp']
    df.columns = cols
    df = df.dropna(subset=['track_id', 'weight_erp'])
    return df

# 储存平川运费数据用以导入ERP


def save_data(df):
    im_erp = df.loc[:, ['track_id', 'weight', 'real_price']]
    im_erp.columns = ['物流单号', '结算重量', '结算运费']
    im_erp.to_excel('导入ERP.xlsx', index=False)
    im_erp.to_clipboard(index=False)

# 获取误差


def get_diff(right, left):
    right.track_id = right.track_id.map(str.upper)
    left.track_id = left.track_id.map(str.upper)
    right = right[right.track_id.isin(left.track_id)]
    right = right.loc[:, ['track_id', 'weight_erp']]
    left = left.loc[:, ['track_id', 'weight']]
    diff = pd.merge(right, left, on='track_id')
    diff['diff'] = diff['weight_erp'] - diff['weight']
    return diff[diff['diff'] < -5]

# 获取在ERP中不在货代中


def get_right(right, left):
    right.track_id = right.track_id.map(str.upper)
    left.track_id = left.track_id.map(str.upper)
    right = right[~right.track_id.isin(left.track_id)]
    right = right.loc[right['carrier'] == '平 川', ['track_id', 'delivery_time']]
    return right

# 获取在货代中不在ERP中


def get_left(right, left):
    right.track_id = right.track_id.map(str.upper)
    left.track_id = left.track_id.map(str.upper)
    left = left[~left.track_id.isin(right.track_id)]
    left = left.loc[:, ['track_id', 'date']]
    return left

if __name__ == '__main__':
    # 文件路径
    path = r"E:\Work\06-Work\00-Todo\Freight\pinchuan"
    file = r'2016-10月叶东东汇总帐单20161026.xls'
    full_path = os.path.join(path, file)
    erp_path = r"E:\Work\06-Work\00-Todo\Self Calc\Freight Self Calc Download\order_detail_export_2016-10-21.xlsx"
    df_carrier = get_carrier_data(full_path)
    df_erp = get_erp_data(erp_path)
    save_data(df_carrier)
    print(df_carrier.groupby('date').sum())
    over = get_diff(df_erp, df_carrier)
    over.to_csv('重量误差.csv', index=False)

    lostable = get_right(df_erp, df_carrier)
    wrong = get_left(df_erp, df_carrier)
    lostable.to_csv('可能遗失.csv', index=False)
    wrong.to_csv('可能混淆.csv', index=False)
    print(get_right(df_erp, df_carrier))
    print(get_left(df_erp, df_carrier))

    # 按小时绘图
    df_erp.index = df_erp.paid_time
#    df_erp['hour'] = df_erp.index.hour
#    sum_df_erp = df_erp.groupby("hour").count()['order_id']
#    print(sum_df_erp)
#    sum_df_erp.plot()

    # 按一周绘图
    df_erp['week'] = df_erp.index.dayofweek
    count_df_erp = df_erp.groupby("week").count()['order_id']
    print(count_df_erp)
    count_df_erp.plot()
