#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
查询目标文件夹大小
Version:    2016-08-19
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import os
from os.path import join, getsize
from multiprocessing import Pool


def getdirsize(dir, path=r'size.csv'):
    for root, dirs, files in os.walk(dir):
        try:
            for name in files:
                filename = join(root, name)
                size = getsize(filename)
                print('There are {0:.3f} Mbytes in {1}'.format(
                    size / 1024 / 1024, filename))
                with open(path, 'a+') as f:
                    f.write('{0:.3f},{1}\n'.format(
                        size / 1024 / 1024, filename))
        except WindowsError:
            pass


if __name__ == '__main__':
    p = Pool()
    for i in ['C:\\', 'd:\\', 'e:\\', 'f:\\']:
        p.apply_async(getdirsize, (i, r'E:\workspace\size.csv'))
    p.close()
    p.join()
