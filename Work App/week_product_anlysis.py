# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-01-20 14:13:56
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-23 16:13:29 
# @email: lucibriel@163.com


import os

import arrow
import numpy as np
import pandas as pd


def get_date(days=0, slash=""):
    return arrow.now().shift(days=-days).format(f"YYYY{slash}MM{slash}DD")


def tidy_number(el):
    if ',' in el:
        return float(el.replace(',', ''))
    if '%' in el:
        return float(el.split("%")[0]) * 10**-2
    return float(el)


def format_date(date):
    return f"{date[:4]}-{date[4:6]}-{date[6:]}"


def cal(df, date=None):
    df['日期'] = get_date(
        2, slash="-") if not date else format_date(date)
    df['R点击率'] = df['访客数'] / df['实际曝光量']
    df['转化率'] = df['买家数'] / df['访客数']
    df['客单价'] = df['支付金额'] / df['买家数']
    df['P4P占比'] = df['P4P'] / (df['支付金额'] * 6.5)
    df['客单价'] = df['客单价'].map(lambda x: round(x, 2))
    formater = '{:.2%}'.format
    df['转化率'] = df['转化率'].map(formater)
    df['R点击率'] = df['R点击率'].map(formater)
    df['P4P占比'] = df['P4P占比'].map(formater)
    return df


def change_type(df, filter_cols=['商品ID', '商品标题', '平台', '商品名称']):
    for i in df.columns:
        if i not in filter_cols:
            df[i] = df[i].map(tidy_number)
    return df


def anlysis(product, promotion, savepath, date=None):
    p_df = pd.read_excel(product)
    p_df = p_df[p_df['平台'] == "TOTAL"]
    promotion_df = pd.read_excel(promotion)

    p_df = change_type(p_df)
    promotion_df = change_type(promotion_df)

    result = pd.merge(p_df, promotion_df, how='outer',
                      left_on='商品标题', right_on='商品名称')
    print(result.shape)
    result.to_csv('test1.csv', index=False)

    output_col = ['日期', '商品ID', '商品标题', '实际曝光量', '浏览量',
                  '访客数', 'R点击率', '转化率', '买家数', '订单数',
                  '支付金额', '客单价', 'P4P', 'P4P占比']
    anlysis = result.sort_values('支付订单数', ascending=False).head(20)
    anlysis.rename(columns={'搜索曝光量': '实际曝光量',
                            '商品页浏览量': '浏览量',
                                      '商品页访客数': '访客数',
                                      '支付买家数': '买家数',
                                      '支付订单数': '订单数',
                                      '花费': 'P4P'}, inplace=True)
    anlysis.ix[anlysis['P4P'].isnull(), 'P4P'] = 0

    anlysis = cal(anlysis, date)
    anlysis = anlysis.ix[:, output_col]
    today = get_date(2, slash="-")
    if date is None:
        anlysis.to_csv(savepath.format(today), index=False)
    else:
        anlysis.to_csv(savepath.format(date), index=False)


def run(date=None):
    if date is None:
        product = f"Product+Analysis {str(get_date())}.xls"
        promotion = f"商品推广 {str(get_date())}.xls"
        anlysis(product, promotion, savepath)
    else:
        product = f"Product+Analysis {date}.xls"
        promotion = f"商品推广 {date}.xls"
        anlysis(product, promotion, savepath, date)


if __name__ == '__main__':
    workpath = r"F:\Work\06-Work\Data Anlysis\03-商品数据\2018"
    savepath = '产品分析_{}.csv'
    os.chdir(workpath)
    print(os.getcwd())
    run()
    # print(product, '\n', promotion)
