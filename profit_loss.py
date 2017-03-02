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
import os 
import pylab as plt 

# 按国家取TOP10
def top10(df,country='United States', startDate='2016-01-01', endDate='2016-08-31'):
    df = df[(startDate < df.paid_time) & (df.paid_time < endDate)]
    return df[df['country'] == country].groupby(['SPU']).sum().sort_values(by='orders', ascending=False)

# 定义函数，获得SPU
def get_spu(item):
    if item.startswith('B9'):
        spu,attr = item[:5],item[5:]
    elif item.startswith('EATGE'):
        spu,attr = item[:11],item[12:]
    elif item.startswith('WZ'):
        spu,attr = item[:9],item[9:]
    else:
        spu,attr = item[:7],item[7:]
        if attr.startswith('-'):
            attr = attr[1:]
    return spu,attr

# 获取分类
def get_cat(item):
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
    sheet_name = 'Single'
    cols = ['erp_id','order_id','img_url','sku','sale_num',
            'carrier','channel','track_number','price','weight',
           'weight_cal','get_money','purchase','freight',
           'package_fee','profit','paid_time','store','ship_time',
           'country'
           ]
    df = pd.read_excel(path, sheet_name, headers=1)
    # 替换标题
    df.columns = cols
    # 类型更换
    df.erp_id = df.erp_id.astype(object)
    df['multi'] = df.sale_num.map(lambda x: 'Y' if x > 1 else 'N')
    df['win'] = df.profit.map(lambda x:'Y' if x > 0 else 'N')
    # 梳理数据
    df['SPU'] = Series([i[0] for i in df.sku.map(get_spu)])
    df['attr'] = Series([i[-1] for i in df.sku.map(get_spu)])
    df['cat'] = df.SPU.map(get_cat)
    df = df.dropna(subset=['get_money','freight'])
    return df


# 按SPU分组汇总，按利润排序
def group(df,columns='SPU'):
    df = df.groupby(columns).sum().sort_values(by='profit')
    df['avg_profit'] = round(df.profit / df.sale_num,2)
    df['avg_price'] = round(df.price / df.sale_num, 2)
    return df

# 绘制散点图
def draw_scatter(x, y):
    plt.scatter(x,y)
    plt.show()

# 存入excel
def save(df, path):   
    excel_name = 'profit.xlsx'
    sheet_name = ['loss','profit','country_loss','store','cat','total']
    cols = ['销量','利润/￥','销售额/￥','单个销售额/￥','单个利润/￥']
    sum_spu = group(df).loc[:,['sale_num','profit','price',
    'avg_price','avg_profit']]
    sum_country = group(df,'country').loc[:,['sale_num','profit','price',
    'avg_price','avg_profit']]
    sum_store = group(df,'store').loc[:,['sale_num','profit','price',
    'avg_price','avg_profit']]
    sum_cat = group(df, 'cat').loc[:,['sale_num','profit','price',
    'avg_price','avg_profit']]
    draw_scatter(sum_spu['sale_num'],sum_spu['profit'])    
    sum_spu.columns = cols
    sum_country.columns = cols
    sum_store.columns = cols
    sum_cat.columns = cols
    full_path = os.path.join(path,excel_name)
    with pd.ExcelWriter(full_path) as writer:
        sum_spu.head(10).to_excel(writer,sheet_name[0])
        sum_spu.tail(10).to_excel(writer,sheet_name[1])
        sum_country.to_excel(writer,sheet_name[2])
        sum_store.to_excel(writer,sheet_name[3])
        sum_cat.to_excel(writer, sheet_name[4])
        sum_spu.to_excel(writer,sheet_name[-1])

if __name__ =='__main__':
    path = r"E:\Work\06-Work\Data Anlysis\Profit Loss\Mon10A_PA\Mon10_product.xls"
    df = get_data(path)
    t_path = r'E:\Work\06-Work\Data Anlysis\Profit Loss\Mon10A_PA'
    save(df, t_path)