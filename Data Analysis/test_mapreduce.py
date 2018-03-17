# -*- coding: utf-8 -*- 
# @Author: Steven 
# @Date: 2018-03-15 09:21:29 
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-16 14:33:00 
# @file: test_mapreduce.py
import xlrd
import collections
from map_reduce import MapReduce
import glob
import operator
import arrow

start_date = arrow.Arrow(2013, 5, 1)
end_date = arrow.Arrow(2013, 6, 1)

def parse_time(time):
    time = str(time).replace('.','-').replace('/','-')
    return arrow.get(time)

def get_index_via_col_name(sheet, col_name):
    '''通过列名获得列序号'''
    col_names = sheet.row_values(0)
    for col in col_names:
        if col_name in col:
            col_name = col
            break
    else:
        return
    index = col_names.index(col_name)
    return index

def get_data_from_col(sheet, col_name):
    index = get_index_via_col_name(sheet, col_name)
    if index:
        return sheet.col_values(index)
    return


def mapper_match(one_file):
    output = []
    pid_data = collections.defaultdict(int)
    try:
        book = xlrd.open_workbook(one_file)
        sheet0 = book.sheet_by_index(0)
        pids = get_data_from_col(sheet0,'订单号')
        names = get_data_from_col(sheet0,'买家名称')
        place_times = get_data_from_col(sheet0,'下单时间')
    except Exception as e:
        print(one_file, e)
    for pid, name, place_time in zip(pids[1:], names[1:], place_times[1:]):
        if pid_data.get(pid):
            pid_data[pid] += 1
        else:
            pid_data[pid] = 1
        if name is None:
            return
        try:
            place_time = parse_time(place_time)
        except Exception as e:
            print(one_file,pid)
        if pid_data[pid] == 1 and start_date < place_time < end_date:
            print(place_time)
            name = name.title()
            output.append((name, 1))
    return output


def reducer_match(item):
    name, occurances = item
    return (name, sum(occurances))


def mapper_count(item):
    _, count = item
    return [(count, 1)]


def reducer_count(item):
    freq, occurances = item
    return (freq, sum(occurances))


if __name__ == '__main__':
    input_files = glob.glob(
        r"F:\Work\06-Work\Data Anlysis\00-订单数据\*\*\*.xls")
    mapper = MapReduce(mapper_match, reducer_match)
    name_freq = mapper(input_files)
    name_freq.sort(key=operator.itemgetter(1), reverse=True)
    for name, count in name_freq:
        print('{0}\t{1}'.format(name, count))
    mapper = MapReduce(mapper_count, reducer_count)
    name_freq = mapper(name_freq)
    name_freq.sort(key=operator.itemgetter(1), reverse=True)
    for freq, count in name_freq:
        print('{0}\t{1}'.format(freq, count))
