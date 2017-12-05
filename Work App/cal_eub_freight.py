# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-05-13 17:14:35
# @Last Modified by:   steven
# @Last Modified time: 2017-12-02 14:29:48
'''
 author: lucibriel@163.com
 fun: 计算E邮宝运费
'''
import pandas as pd
import os


class Epacket:

    def __init__(self):
        path = os.path.join(os.path.split(__file__)[0], "epacket.xlsx")
        df = pd.read_excel(path)
        df['country'] = df['country'].str.split(',')
        self.df = df

    def __calcs__(self, country):
        is_country = self.df['country'].map(lambda x: country in x)
        calcs = self.df[is_country].T.to_dict()[self.df[is_country].index[0]]
        return calcs

    def get_price(self, country, weight):
        calcs = self.__calcs__(country)
        if weight <= calcs['first_weight']:
            price = calcs['r1_price'] * \
                calcs['first_weight'] + calcs['r1_handle']
        elif weight <= calcs['mid_weight']:
            price = calcs['r1_price'] * weight + calcs['r1_handle']
        else:
            price = calcs['r2_price'] * weight + calcs['r2_handle']
        return price


def test():
    os.chdir(r"F:\workspace")
    path = r"Epacket.xlsx"
    df = pd.read_excel(path)
    eub = Epacket()
    freight = []
    for track in df['快递单号']:
        is_track = df['快递单号'] == track
        country = df[is_track]['国家'].values[0].lower()
        weight = df[is_track]['实际重量(g)'].values[0]
        try:
            cost = eub.get_price(country, weight)
            print(cost)
            freight.append(cost)
        except:
            print(track)
    # print(freight)
    df['结算运费'] = pd.Series(freight)
    df = df.loc[:, ['快递单号', '实际重量(g)', '结算运费']]
    df.columns = ['物流单号', '结算重量', '结算运费']
    df.to_csv("计算结果.csv", index=False)
    df.to_clipboard(index=False)

if __name__ == '__main__':
    test()
    # print(calc_eub('france', 899))
