# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-09-05 15:02:45
# @Last Modified by:   steven
# @Last Modified time: 2017-10-31 14:26:31
import glob
import os
import pandas as pd
from multiprocessing import Pool


def get_files(path):
    return glob.glob(path)


def parse_data(file):
    xlsx = pd.ExcelFile(file)
    if len(xlsx.sheet_names) > 1:
        df = pd.read_excel(xlsx, 1)
        if '物流单号' not in df.columns:
            df['物流单号'] = df['运单号']
            df['结算重量'] = df['重量(g)']
            df['结算运费'] = df['账单金额']
    else:
        df = pd.read_excel(xlsx)
        if '物流单号' not in df.columns:
            df['物流单号'] = df['快递单号']
            df['结算重量'] = df['重量']
            df['结算运费'] = df['汇总金额']
    return df


def save(file):
    filename = os.path.basename(file)
    print(f'Handle: {filename}')
    df = parse_data(file)
    df.to_excel(file, index=False)
    print(f'Done: {filename}')

if __name__ == '__main__':
    path = r'E:\Work\06-Work\00-Todo\Freight\燕文\*.xl*'
    p = Pool()
    for file in get_files(path):
        p.apply_async(save, (file,))
    p.close()  # 关闭进程池，表示不能在往进程池中添加进程
    p.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用
    # file = r"E:\Work\06-Work\00-Todo\Freight\燕文\27000484(2017-10-23_2017-10-29).xlsx"
    # df = parse_data(file)
    # # print(xlsx.sheet_names)
    # print(df.head())
