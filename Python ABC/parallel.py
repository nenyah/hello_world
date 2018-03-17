# -*- coding: utf-8 -*- 
# @Author: Steven 
# @Date: 2018-03-15 08:51:46 
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-15 09:02:21 
# @file: parallel.py
import os
import time
from multiprocessing import Pool


def task(args):
    time.sleep(1)
    pid = os.getpid()
    return pid, args


if __name__ == '__main__':
    start = time.time()
    p = Pool(5)
    result = p.map(task, range(10))
    print(result)
    print('Cost: {0}'.format(time.time()-start))
