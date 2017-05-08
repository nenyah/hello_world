# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:09:43 2017

@author: steve
"""

import pandas as pd
import numpy as np
import datetime

product = r"E:\Work\06-Work\Data Anlysis\03-商品数据\Product+Analysis 20170330.xls"
promotion = r"E:\Work\06-Work\Data Anlysis\03-商品数据\商品推广20170330.xls"

p_df = pd.read_excel(product)
p_df = p_df.set_index(p_df['商品标题'])
promotion_df = pd.read_excel(promotion)
promotion_df = promotion_df.set_index(promotion_df['商品名称'])
result = pd.concat([p_df,promotion_df],axis=1)

col = ['商品ID','商品标题','搜索曝光量','商品页浏览量',
       '商品页访客数','支付买家数','支付订单数','支付金额','花费']
new_col = ['商品ID','商品标题','曝光量','浏览量',
   '访客数','买家数','订单数','支付金额','P4P']
output_col = ['日期','商品ID','商品标题','曝光量','浏览量',
   '访客数','点击率','转化率','买家数','订单数',
   '支付金额','客单价','P4P','P4P占比']
anlysis = result.sort_values('支付订单数',ascending=False)[col].head(20)
anlysis.columns = new_col
anlysis['日期'] = datetime.date.today() - datetime.timedelta(days=2)
anlysis['点击率'] = anlysis['访客数']/anlysis['曝光量']
anlysis['转化率'] = anlysis['买家数']/anlysis['访客数']
anlysis['客单价'] = anlysis['支付金额']/anlysis['买家数']
anlysis['P4P占比'] = anlysis['P4P']/(anlysis['支付金额']*6.5)
anlysis['客单价'] = anlysis['客单价'].map(lambda x: round(x,2))
anlysis['转化率'] = anlysis['转化率'].map('{:.2%}'.format)
anlysis['点击率'] = anlysis['点击率'].map('{:.2%}'.format)
anlysis['P4P占比'] = anlysis['P4P占比'].map('{:.2%}'.format)
anlysis = anlysis.ix[:, output_col]
date = datetime.date.today() - datetime.timedelta(days=2)
anlysis.to_csv(r'E:\Work\06-Work\Data Anlysis\03-商品数据\产品分析_{0}.csv'.format(date), index=False)