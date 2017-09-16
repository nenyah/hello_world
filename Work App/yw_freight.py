# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-09-05 15:02:45
# @Last Modified by:   steven
# @Last Modified time: 2017-09-16 16:09:26
import glob
import os
import pandas as pd
from multiprocessing import Pool


def get_files(path):
    return list(glob.glob(path))


def parse_data(file):
    df = pd.read_excel(file)
    if '物流单号' not in df.columns:
        df['物流单号'] = df['快递单号']
        df['结算重量'] = df['重量']
        df['结算运费'] = df['汇总金额']
    return df


def save(file):
    filename = os.path.basename(file)
    print(f'Handle: {filename}')
    df = parse_data(file)
    df.to_excel(file)
    print(f'Done: {filename}')

if __name__ == '__main__':
    path = r'E:\Work\06-Work\00-Todo\Freight\燕文\*.xls'
    p = Pool()
    for file in get_files(path):
        p.apply_async(save, (file,))
    p.close()  # 关闭进程池，表示不能在往进程池中添加进程
    p.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用
