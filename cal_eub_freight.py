'''
 author: lucibriel@163.com
 date: 2017-05-06
 fun: 计算E邮宝运费
'''
import pandas as pd
import os


def get_ref(country):
    path = os.path.join(os.path.split(__file__)[0], "epacket.xlsx")
    df = pd.read_excel(path)
    df['country'] = df['country'].str.split(',')
    is_country = df['country'].map(lambda x: country in x)
    calcs = df[is_country].T.to_dict()[df[is_country].index[0]]
    return calcs


def calc_eub(country, weight):
    calcs = get_ref(country)
    if weight <= calcs['first_weight']:
        return calcs['r1_price'] * calcs['first_weight'] + calcs['r1_handle']
    elif weight <= calcs['mid_weight']:
        return calcs['r1_price'] * weight + calcs['r1_handle']
    else:
        return calcs['r2_price'] * weight + calcs['r2_handle']


if __name__ == '__main__':
    print(calc_eub('sa', 40))
