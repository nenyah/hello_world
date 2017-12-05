#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-03-04 14:43:55
# @email: lucibriel@163.com
# @Last Modified by:   steven
# @Last Modified time: 2017-09-30 14:00:47
import os
import sys
import pandas as pd


def get_file_names(path):
    """get all file name in path"""
    for i in os.walk(path):
        for filename in i[-1]:
            full_filename = os.path.join(i[0], filename)
            yield full_filename


def merge_excel_from_sheets(xls, on=None):
    """merge excel all sheets"""
    xlsx = pd.ExcelFile(xls)
    df = dict()
    for name in xlsx.sheet_names:
        df[name] = pd.read_excel(xlsx, name)
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


def merge_excel(path, remove_duplicate=False, on=None):
    """merge excel not matter single file or path"""
    if not os.path.exists(path):
        print("Path dosen't exists")
        return None
    if is_xls(path):
        df = merge_excel_from_sheets(path)

    if os.path.isdir(path):
        files = get_file_names(path)
        df = dict()
        for file in files:
            if is_xls(file):
                df[file] = merge_excel_from_sheets(file)
        df = pd.concat(df, axis=0)
        df = df.dropna(thresh=5)
        if remove_duplicate:
            df = df.drop_duplicates(on)
    return df


if __name__ == '__main__':
    path = r'E:\Work\06-Work\00-Todo\线上运费\20170905'
    df = merge_excel_from_path(path)
    save(df)
