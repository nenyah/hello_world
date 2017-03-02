#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 登陆知乎测试
__author__ = 'Steven Tan'
#导入必要的库
import requests
from bs4 import BeautifulSoup
def login_zhihu(user,password):
	headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	url = 'https://www.zhihu.com/#signin'
	session = requests.Session() #实例化Session
	wb_data = session.get(url,headers=headers).text
	soup = BeautifulSoup(wb_data,'lxml')
	# 填写登录表单
	xsrf = soup.select('input[value]')[-1].get('value')
	data = {
	    '_xsrf': xsrf,
	    'password': password,
	    'remember_me': 'true',
	    'email': user
	}
	# 提交表单
	log_post =session.post('http://www.zhihu.com/login/email', data=data)
	url = 'https://www.zhihu.com/'
	test = session.get(url)
	wb_data = BeautifulSoup(test.text, 'lxml')
	# 检验是否成功登录
	content = wb_data.select('h2 > a')
	print(content)
	print(len(content))

if __name__ == '__main__':
	user = input('Please enter your email:\n')
	pwd = input('Please enter your password:\n')
	login_zhihu(user,pwd)
