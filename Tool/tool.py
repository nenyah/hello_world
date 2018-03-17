# -*- coding: utf-8 -*- 
# @Author: Steven 
# @Date: 2017-12-19 13:55:23 
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-16 14:23:14 
# @file: tool.py
import os
import sys
from pathlib import Path

import pandas as pd


def get_file_names(path, keyword=None, pedix=None):
    """get all file name in path"""
    p = Path(path)
    if pedix:
        return p.glob(f'**/*{keyword}*.{pedix}*')
    return p.glob(f'**/*{keyword}*.*')


def merge_excel_from_sheets(xls, on=None):
    """merge excel all sheets"""

    xlsx = pd.ExcelFile(xls)
    df = dict()
    for name in xlsx.sheet_names:
        df[name] = pd.read_excel(xlsx, name)
        if len(df[name].columns) not in [26,27,28]:
            print(xls)
            print(len(df[name].columns))
    df = pd.concat(df, axis=0)
    if on:
        return df.drop_duplicates(on)
    else:
        return df


def is_xls(path):
    """judge is excel format file"""
    return os.path.splitext(path)[-1] in ['.xls', '.xlsx']


def save(df, save_path=None):
    """save data"""
    if save_path:
        df.to_csv(save_path, index=False)
    df.to_csv(os.path.join(path, "total.csv"), index=False)


def merge_excel(path, keyword=None, pedix=None, remove_duplicate=None):
    """merge excel not matter single file or path"""
    p = Path(path)
    if not p.exists():
        print("Path dosen't exists")
        return None
    if is_xls(path):
        df = merge_excel_from_sheets(path)

    if p.is_dir():
        files = get_file_names(path, keyword, pedix)
        df = dict()
        for file in files:
            df[file] = merge_excel_from_sheets(file)
        df = pd.concat(df, axis=0)
        df = df.dropna(thresh=5)
        if remove_duplicate:
            df = df.drop_duplicates(remove_duplicate)
    return df


if __name__ == '__main__':
    path = r'F:\Work\06-Work\Data Anlysis\00-订单数据'
    df = merge_excel(path, keyword="2",pedix="xls",remove_duplicate='订单号')
    print(len(df))
    # save(df)
