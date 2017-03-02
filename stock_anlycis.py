#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
根据现有数据求目标成本或根据目标成本求买入价和量
Version:    2016-08-23
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
def get_new_cost(prices_pair):
	"""compute the new cost by given prices pair

	Keyword arguments:
    prices_pair -- the price pair (default 0,0.0)
	return:
	new cost float
	"""
	sum_expenditure,num = 0,0
	sum_expenditure = sum([x[0]*x[-1] for x in prices_pair])
	num = sum([x[0] for x in prices_pair])
	return round(sum_expenditure / num,2)


def get_cost(buy_volumn,price,number,old_cost):
	""" compute the new cost by given prices
	buy_volumn: int position 买入量,
	price: float buy price 买入价,
	number: int position 持仓,
	old_cost: float cost 成本,
	return: float new cost 新成本
	"""
	return (buy_volumn * price + number * old_cost) / (buy_volumn + number)

def get_volumn(number,old_cost,target_cost):
	"""根据给定的持仓量、历史成本、目标成本求买入量和价和投入
	number: int position 持仓,
	old_cost: float cost 历史成本,
	target_cost: float target cost 目标成本,
	yield: int buy volumn 买入量, float buy price 买入价, float 总投入
	"""
	buy_volumn = 0
	buy_price = target_cost
	for x in range(100,20000,100):
		buy_volumn = x
		buy_price = (target_cost*(number + buy_volumn) - number * old_cost) / buy_volumn
		if 0 < buy_price < target_cost and x*buy_price <= 50000:
			yield buy_volumn,round(buy_price,2),round(buy_volumn*buy_price,2)
		

	

if __name__ == '__main__':
	for i in get_volumn(100,42.226,17.05):
		print(i)