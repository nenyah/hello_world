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
import arrow


def top10(df, country='United States', startDate='2016-01-01', endDate='2016-08-31'):
    """按国家取TOP10"""
    df = df[(startDate < df.paid_time) & (df.paid_time < endDate)]
    return df[df['country'] == country].groupby(['SPU']).sum().sort_values(by='orders', ascending=False)


def get_cat(item):
    """获取分类"""
    item = str(item)
    return item[:2]


def get_data(path):
    """导入表格，做预处理"""
    cols = ['erp_id', 'order_id', 'img_url', 'SKU列表',
            'courier', 'channel', 'track_number', 'price', 'weight',
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
    df['SPU'] = df.sku.map(lambda x: x[:7])
    df['attr'] = df.sku.map(lambda x: x[7:].split("-")[-1])
    df['cat'] = df.SPU.map(get_cat)
    df = df.dropna(subset=['get_money', 'freight'])
    return df


def group(df, columns='SPU'):
    """按SPU分组汇总，按利润排序"""
    df = df.groupby(columns).sum().sort_values(by='profit')
    df['avg_profit'] = round(df.profit / df.sale_num, 2)
    df['avg_price'] = round(df.price / df.sale_num, 2)
    df['profit_rate'] = round(df.profit / df.price, 4)
    df['profit_rate'] = df['profit_rate'].map(lambda x: '{}%'.format(x * 100))
    return df


def draw_scatter(x, y):
    """绘制散点图"""
    today = arrow.now().format('MM-DD')
    plt.scatter(x, y)
    plt.xlabel("sale num")
    plt.ylabel("profit")
    xmin, xmax, ymin, ymax = int(min(x)), int(max(x)), int(min(y)), int(max(y))
    xmid = (xmin + xmax) / 10
    ymid = (ymin + ymax) / 10
    plt.axis([xmin - xmid, xmax + xmid, ymin - ymid, ymax + ymid])
    plt.savefig(today + " profit.png", format='png', dpi=300)


def save(df, path):
    """存入excel"""
    this_month = arrow.now().month
    excel_name = f'Mon {str(this_month)} profit.xlsx'
    sheet_name = ['loss', 'profit', 'country_loss',
                  'store', 'cat', 'courier', 'total']
    cols = ['销量', '利润/￥', '销售额/￥', '单个销售额/￥', '单个利润/￥', '利润率']
    out_cols = ['sale_num', 'profit', 'price',
                'avg_price', 'avg_profit', 'profit_rate']
    sum_spu = group(df).loc[:, out_cols]
    sum_country = group(df, 'country').loc[:, out_cols]
    sum_store = group(df, 'store').loc[:, out_cols]
    sum_cat = group(df, 'cat').loc[:, out_cols]
    sum_courier = group(df, 'courier').loc[:, out_cols]
    draw_scatter(sum_spu['sale_num'], sum_spu['profit'])
    sum_courier.columns = cols
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
        sum_courier.to_excel(writer, sheet_name[5])
        sum_spu.to_excel(writer, sheet_name[-1])

if __name__ == '__main__':
    os.chdir(r"E:\Work\06-Work\Data Anlysis\Profit Loss\2017")
    path = r".\Mon08\Mon08_product.xls"
    df = get_data(path)
    today = arrow.now().format('MM-DD')
    df.to_csv(today + " test.csv", index=False)
    t_path = r'.\Mon08'
    save(df, t_path)
