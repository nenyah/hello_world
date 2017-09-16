#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-03-04 14:43:55
# @email: lucibriel@163.com
# @Last Modified by:   steven
# @Last Modified time: 2017-09-13 17:12:00
import os
import sys
import pandas as pd


def get_file_names(path):
    filenames = []
    for i in os.walk(path):
        for filename in i[-1]:
            full_filename = os.path.join(i[0], filename)
            filenames.append(full_filename)
    return filenames


def get_data_from_path(path, on=None):
    """合并数据"""
    xlsx = pd.ExcelFile(path)
    df = dict()
    for name in xlsx.sheet_names:
        df[name] = pd.read_excel(xlsx, name)
        # print(len(df[name]))
    data = pd.concat(df, axis=0)
    if on:
        return data.drop_duplicates(on)
    else:
        return data


def merge_excel(path, save_path=None, remove_duplicate=True):
    if not os.path.exists(path):
        print("Path dosen't exists")
        return None
    if os.path.splitext(path)[-1] in ['.xls', '.xlsx']:
        df = get_data_from_path(path)

    if os.path.isdir(path):
        files = get_file_names(path)
        df = list(map(get_data_from_path, files))
        df = pd.concat(df, axis=0)
        df = df.dropna(thresh=5)
        if remove_duplicate:
            df = df.drop_duplicates(df.columns[1])
    if save_path:
        df.to_csv(save_path, index=False)
    else:
        df.to_csv(os.path.join(path, "total.csv"), index=False)
    return df

if __name__ == '__main__':
    path = r'E:\Work\06-Work\00-Todo\线上运费\20170905'
    df = merge_excel(path)
