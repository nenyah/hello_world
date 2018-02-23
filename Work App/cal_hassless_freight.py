# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-09-29 14:12:36
# @Last Modified by:   Steven
# @Last Modified time: 2017-12-22 15:41:53
'''
 author: lucibriel@163.com
 fun: 计算无忧运费
'''
import os

import pandas as pd


class Hassless:
    """docstring for Hassless"""

    def __init__(self,):
        path = os.path.join(os.path.split(__file__)[0], "hassless.xlsx")
        df = pd.read_excel(path, keep_default_na=False)
        df['country'] = df['country_name_en'].str.lower() + ',' + \
            df['country_name_abbrev'].str.lower() + ',' + df['country_name_cn']

        df['country'] = df['country'].str.split(',')
        self.df = df

    def __calcs(self, country):
        is_country = self.df['country'].map(lambda x: country in x)
        calcs = self.df[is_country].T.to_dict()[self.df[is_country].index[0]]
        return calcs

    def get_price(self, country, weight):
        calcs = self.__calcs(country)
        price = calcs['price']*weight*0.001 + calcs['handle']
        return price


if __name__ == '__main__':
    h = Hassless()
    print(h.get_price('us', 800))
