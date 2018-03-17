# -*- coding: utf-8 -*- 
# @Author: Steven 
# @Date: 2018-03-15 09:06:53 
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-15 09:59:03 
# @file: map_reduce.py
import collections
import itertools
import multiprocessing


class MapReduce:
    """docstring for MapReduce"""

    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        partition_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partition_data[key].append(value)
        return partition_data.items()

    def __call__(self, inputs, chunksize=1):
        map_responses = self.pool.map(
            self.map_func, inputs, chunksize=chunksize)
        partition_data = self.partition(itertools.chain(*map_responses))
        reduce_values = self.pool.map(self.reduce_func, partition_data)
        return reduce_values
