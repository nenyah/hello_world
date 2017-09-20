#-*- coding: utf-8 -*-
import pandas as pd
from apriori import * #导入自行编写的apriori函数
import time #导入时间库用来计算用时

inputfile = r"C:\Users\steve\Desktop\Temp\关联产品研究.csv" #输入事务集文件
data = pd.read_csv(inputfile, header=None, dtype = object)

start = time.clock() #计时开始
print('\n转换原始数据至0-1矩阵...')
ct = lambda x : pd.Series(1, index = x[pd.notnull(x)]) #转换0-1矩阵的过渡函数
b = map(ct, data.as_matrix()) #用map方式执行
data = pd.DataFrame(list(b)).fillna(0) #实现矩阵转换，空值用0填充
print(data)
end = time.clock() #计时结束
print('\n转换完毕，用时：{0:0.2f}秒'.format((end-start)))
del b #删除中间变量b，节省内存

support = 0.05 #最小支持度
confidence = 0.75 #最小置信度
ms = '---' #连接符，默认'--'，用来区分不同元素，如A--B。需要保证原始表格中不含有该字符

start = time.clock() #计时开始
print('\n开始搜索关联规则...')
find_rule(data, support, confidence, ms)
end = time.clock() #计时结束
print('\n搜索完成，用时：{0:0.2f}秒'.format((end-start)))