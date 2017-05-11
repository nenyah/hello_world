#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import os
import glob

os.chdir("F:\workspace")
# 获取路径内所有文件


def get_file_names(path):
    filenames = []
    for i in os.walk(path):
        for filename in i[-1]:
            full_filename = os.path.join(i[0], filename)
            filenames.append(full_filename)
    return filenames


# 获取目标目录所有
def get_data_from_path(path, on="产品编号"):
    """合并数据"""
    xlsx = pd.ExcelFile(path)
    df = dict()
    for name in xlsx.sheet_names:
        df[name] = pd.read_excel(xlsx, name)
        print(len(df[name]))
    data = pd.concat(df, axis=0)
    if on:
        return data.drop_duplicates(on)
    else:
        return data


if __name__ == "__main__":
    col = "产品编号	供应商	供应商型号	国内运费（CNY）	备注	备用网址	异常备注	汇率	类别材质尺寸	采购价(CNY)	重量(KG)	链接".split(
    )
    path = r"E:\01-采购管理\采购表汇总\户外"
    files = get_file_names(path)
    df = list(map(get_data_from_path, files))
    df = pd.concat(df, axis=0)
    print(len(df))
    print(df.columns)
    df = df[col]

    print(col)
    print(df.head(1))
    df.to_csv("test.csv", index=False)
