# -*- coding: utf-8 -*- 
# @Author: Steven 
# @Date: 2018-03-15 09:30:41 
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-15 09:35:57 
# @file: test_xlrd.py
import xlrd
xlsfile = r"F:\Work\06-Work\Data Anlysis\00-订单数据\2018订单数据\0-MF\20180101_20180201.xls"  # 打开指定路径中的xls文件
book = xlrd.open_workbook(xlsfile)  # 得到Excel文件的book对象，实例化对象
sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象
print("1、", sheet0)
sheet_name = book.sheet_names()[0]  # 获得指定索引的sheet表名字
print("2、", sheet_name)
sheet1 = book.sheet_by_name(sheet_name)  # 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
nrows = sheet0.nrows    # 获取行总数
print("3、", nrows)
# 循环打印前三行的内容
for i in range(3):
    print(f'  - [{i}]',sheet1.row_values(i))
ncols = sheet0.ncols  # 获取列总数
print("4、", ncols)
row_data = sheet0.row_values(0)     # 获得第1行的数据列表
print(row_data)
col_data = sheet0.col_values(0)     # 获得第1列的数据列表
print("5、", col_data)
# 通过坐标读取表格中的数据
cell_value1 = sheet0.cell_value(0, 0)
print("6、", cell_value1)
cell_value2 = sheet0.cell_value(0, 1)
print("7、", cell_value2)
