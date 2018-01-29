# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-01-20 14:13:56
# @Last Modified by:   Steven
# @Last Modified time: 2018-01-05 15:28:20
# @email: lucibriel@163.com


import pandas as pd
import numpy as np
import arrow
import os


def get_date(days=0, slash=""):
    return arrow.now().shift(days=-days).format(f"YYYY{slash}MM{slash}DD")


def tidy_number(el):
    el = str(el)
    if ',' in el:
        return float(el.replace(',', ''))
    if '%' in el:
        return float(el.split("%")[0]) * 10**-2
    return float(el)


def cal(df):
    df['日期'] = get_date(2, slash="-")
    df['R点击率'] = df['访客数'] / df['实际曝光量']
    df['转化率'] = df['买家数'] / df['访客数']
    df['客单价'] = df['支付金额'] / df['买家数']
    df['P4P占比'] = df['P4P'] / (df['支付金额'] * 6.5)
    df['客单价'] = df['客单价'].map(lambda x: round(x, 2))
    df['转化率'] = df['转化率'].map('{:.2%}'.format)
    df['R点击率'] = df['R点击率'].map('{:.2%}'.format)
    df['P4P占比'] = df['P4P占比'].map('{:.2%}'.format)
    return df


def change_type(df, filter_cols=['商品ID', '商品标题', '平台', '商品名称']):
    for i in df.columns:
        if i not in filter_cols:
            df[i] = df[i].map(tidy_number)
    return df


def anlysis(product, promotion, savepath):
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

    anlysis = cal(anlysis)
    anlysis = anlysis.ix[:, output_col]
    date = get_date(2, slash="-")
    anlysis.to_csv(savepath.format(date), index=False)


if __name__ == '__main__':
    workpath = r"F:\Work\06-Work\Data Anlysis\03-商品数据\2018"
    savepath = '产品分析_{}.csv'
    os.chdir(workpath)
    print(os.getcwd())
    product = f"Product+Analysis {str(get_date())}.xls"
    promotion = f"商品推广 {str(get_date())}.xls"
    anlysis(product, promotion, savepath)
    # print(product, '\n', promotion)
