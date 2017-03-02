#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
抓取糗事百科文字内容
Version:    2016-06-13
Author:     Steven
Contact:    lucibriel (at) 163.com
"""

import requests
from bs4 import BeautifulSoup

def get_qiushi(page=1):
	"""抓取糗事百科文字内容
	Parameter：
	page -- 页码
	"""
	
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
		'Connection':'keep-alive'
	}

	url = 'http://www.qiushibaike.com/hot/page/{}'.format(str(page))
	web_data = requests.get(url,headers=headers)
	soup = BeautifulSoup(web_data.text,'lxml')

	usrs = soup.select('.article h2')
	contents = soup.select('.article .content')
	votes = soup.select('.article .stats-vote .number')
	comments = soup.select('.article .stats-comments .number')

	for usr, content, vote, comment in zip(usrs,contents,votes,comments):
		print('用户:',usr.text.strip())
		print('内容:',content.text.strip())
		print('好笑：{}\t评论：{}'.format(vote.text.strip(),comment.text.strip()))
		print('='*50)

if __name__ == '__main__':
	get_qiushi()