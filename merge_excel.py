#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
合并目录下的所有excel文件，去重后存入新的excel
Version:    2016-10-10
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
 
import os
import glob
import pandas as pd
 
 
# 攻取目标目录所有
def get_data(path=r'./*.xls', on=None):
    """合并数据"""
    all_data = pd.DataFrame()
    for f in glob.glob(path):
        df = pd.read_excel(f)
#        print(len(df))
        all_data = all_data.append(df, ignore_index=True)
    if on:
        return all_data.drop_duplicates(on)
    else:
        return all_data
 
 
if __name__ == '__main__':
    print('Program is running...')
    path = r'E:\Work\06-Work\00-Todo\Self Calc\Freight Self Calc Download\*'
    target_path = r'E:\Work\06-Work\00-Todo\Self Calc\Freight Self Calc Sort'
 
    df = get_data(path)
    df.to_excel(os.path.join(target_path,"Total.xlsx"),index=False)
    print('Success!')