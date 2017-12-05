# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-09-29 14:12:36
# @Last Modified by:   steven
# @Last Modified time: 2017-09-29 16:52:34
'''
 author: lucibriel@163.com
 fun: 计算无忧运费
'''
import pandas as pd
import os


def get_ref(country):
    path = os.path.join(os.path.split(__file__)[0], "hassless.xlsx")
    df = pd.read_excel(path)
    df['country'] = df['country_name_en'].str.lower() + ',' + \
        df['country_name_abbrev'].str.lower() + ',' + df['country_name_cn']

    df['country'] = df['country'].str.split(',')
    # [print(type(i)) for i in df['country']]
    is_country = df['country'].map(lambda x: country in x)
    print(is_country)
    # calcs = df[is_country].T.to_dict()[df[is_country].index[0]]
    # return calcs
if __name__ == '__main__':
    get_ref('us')
