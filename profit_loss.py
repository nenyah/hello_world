#! /user/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Function:
根据ERP导出利润数据做产品盈亏分析
Version:    2016-09-09
Author:     Steven
Contact:    lucibriel (at) 163.com
"""


import pandas as pd
from pandas import Series
import numpy as np
import os
import matplotlib.pyplot as plt

# 按国家取TOP10


def top10(df, country='United States', startDate='2016-01-01', endDate='2016-08-31'):
    df = df[(startDate < df.paid_time) & (df.paid_time < endDate)]
    return df[df['country'] == country].groupby(['SPU']).sum().sort_values(by='orders', ascending=False)

# 定义函数，获得SPU


def get_spu(item):
    if item.startswith('B9'):
        spu, attr = item[:5], item[5:]
    elif item.startswith('EATGE'):
        spu, attr = item[:11], item[12:]
    elif item.startswith('WZ'):
        spu, attr = item[:9], item[9:]
    else:
        spu, attr = item[:7], item[7:]
        if attr.startswith('-'):
            attr = attr[1:]
    return spu, attr

# 获取分类


def get_cat(item):
    item = str(item)
    if item.startswith('B9'):
        return 'B9'
    elif item.startswith('EATGE'):
        return 'EATGE'
    elif item.startswith('WZ'):
        return 'WZ'
    else:
        return item[:2]

# 导入表格，做预处理


def get_data(path):
    cols = ['erp_id', 'order_id', 'img_url', 'SKU列表',
            'carrier', 'channel', 'track_number', 'price', 'weight',
            'weight_cal', 'get_money', 'purchase', 'freight',
            'package_fee', 'profit', 'paid_time', 'store', 'ship_time',
            'country'
            ]
    df = pd.read_excel(path, headers=1)
    # 替换标题
    df.columns = cols
    df = df[~df['SKU列表'].str.contains('<br/>')]
    df['SKU列表'] = df['SKU列表'].str.split("*")
    df['sku'] = df['SKU列表'].map(lambda x: x[0])
    df['sale_num'] = df['SKU列表'].map(lambda x: x[-1])
    del df['SKU列表']

    # 类型更换
    df.erp_id = df.erp_id.astype(object)
    df['sale_num'] = df['sale_num'].astype(np.number)
    df['multi'] = df.sale_num.map(lambda x: 'Y' if x > 1 else 'N')
    df['win'] = df.profit.map(lambda x: 'Y' if x > 0 else 'N')
    # 梳理数据
    df['SPU'] = Series([i[0] for i in df.sku.map(get_spu)])
    df['attr'] = Series([i[-1] for i in df.sku.map(get_spu)])
    df['cat'] = df.SPU.map(get_cat)
    df = df.dropna(subset=['get_money', 'freight'])
    return df


# 按SPU分组汇总，按利润排序
def group(df, columns='SPU'):
    df = df.groupby(columns).sum().sort_values(by='profit')
    df['avg_profit'] = round(df.profit / df.sale_num, 2)
    df['avg_price'] = round(df.price / df.sale_num, 2)
    return df

# 绘制散点图


def draw_scatter(x, y):
    plt.scatter(x, y)
    plt.xlabel("sale num")
    plt.ylabel("profit")
    xmin, xmax, ymin, ymax = int(min(x)), int(max(x)), int(min(y)), int(max(y))
    xmid = (xmin + xmax) / 10
    ymid = (ymin + ymax) / 10
    plt.axis([xmin - xmid, xmax + xmid, ymin - ymid, ymax + ymid])
    plt.savefig("profit.png", format='png', dpi=300)

# 存入excel


def save(df, path):
    excel_name = 'profit.xlsx'
    sheet_name = ['loss', 'profit', 'country_loss', 'store', 'cat', 'total']
    cols = ['销量', '利润/￥', '销售额/￥', '单个销售额/￥', '单个利润/￥']
    sum_spu = group(df).loc[:, ['sale_num', 'profit', 'price',
                                'avg_price', 'avg_profit']]
    sum_country = group(df, 'country').loc[:, ['sale_num', 'profit', 'price',
                                               'avg_price', 'avg_profit']]
    sum_store = group(df, 'store').loc[:, ['sale_num', 'profit', 'price',
                                           'avg_price', 'avg_profit']]
    sum_cat = group(df, 'cat').loc[:, ['sale_num', 'profit', 'price',
                                       'avg_price', 'avg_profit']]
    draw_scatter(sum_spu['sale_num'], sum_spu['profit'])
    sum_spu.columns = cols
    sum_country.columns = cols
    sum_store.columns = cols
    sum_cat.columns = cols
    full_path = os.path.join(path, excel_name)
    with pd.ExcelWriter(full_path) as writer:
        sum_spu.head(10).to_excel(writer, sheet_name[0])
        sum_spu.tail(10).to_excel(writer, sheet_name[1])
        sum_country.to_excel(writer, sheet_name[2])
        sum_store.to_excel(writer, sheet_name[3])
        sum_cat.to_excel(writer, sheet_name[4])
        sum_spu.to_excel(writer, sheet_name[-1])

if __name__ == '__main__':
    os.chdir(r"E:\Work\06-Work\Data Anlysis\Profit Loss\2017")
    path = r".\Mon06\Mon06_product.xls"
    df = get_data(path)
    t_path = r'.\Mon06'
    save(df, t_path)
