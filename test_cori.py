#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
协程 Demo
Version:    2016-07-22
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
from multiprocessing import Pool
import time


def f(x, y):
    return x * x + y

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # start 4 worker processes
        # evaluate "f(10)" asynchronously in a single process
        result = pool.apply_async(f, (10, 20))
        # prints "100" unless your computer is *very* slow
        print(result.get(timeout=1))
