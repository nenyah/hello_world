# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:06:27 2017

@author: steve
@func: 整理线上运费
"""
import sys
sys.path.append("..")
import glob
import pandas as pd
from Tool.tool import merge_excel


# 整理数据
def tidy_data(df):
    # 退货保险项重量置0
    df.loc[df['费用项'] == '退货保险费', '订单重量'] = 0
    # 订单重量单位转换成g
    df['订单重量'] = df['订单重量'] * 1000
    group_df = df.groupby('国际物流单号').sum()[['订单重量', '金额（CNY）']]
    group_df.index.name = '物流单号'
    group_df.columns = ['结算重量', '结算运费']
    return group_df

if __name__ == '__main__':
    path = r'E:\Work\06-Work\00-Todo\线上运费\20170905'
    df = merge_excel(path)
    df = tidy_data(df)
    print(df)
    df.to_clipboard()
