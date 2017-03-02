# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:41:56 2016

@author: steve
"""

import requests
from bs4 import BeautifulSoup
import pymongo
from multiprocessing import Pool
import time
from crawler_tool import request

client = pymongo.MongoClient('localhost', 27017)
fangcan = client['fangcan']
urls_list = fangcan['urls_list']
item_info = fangcan['item_info']



def get_list_url(url):
    data = []
    web = request.get(url, 3)
    soup = BeautifulSoup(web.text, 'lxml')

    max_page = soup.select('.PagerCss a')[-1]['href'].split('=')[-1]

    for page in range(1, int(max_page) + 1):
        list_url = 'http://newhouse.cnnbfdc.com/lpxx.aspx?p={}'.format(str(page))
        html = requests.get(list_url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        all_a = soup.select(".sp_zi12c")
        for a in all_a:
            title = a.text.strip()
            href = 'http://newhouse.cnnbfdc.com/' + a['href']
            info = {'name': title, 'url': href}
            print('Get list info: {}'.format(info))
            urls_list.insert_one(info)
    #         print(info)
    #         data.append(info)
    # return data



def get_detail(page_url):
    html = request.get(page_url, 3)
    detail = BeautifulSoup(html.text, 'lxml')
    item_names = [info.text.strip().replace('：', '') for info in detail.select('.sp_f12')][:30]
    if '地图定位' in item_names:
        item_names.remove('地图定位')
    item_content = [info.text.strip().replace(' ', '').replace('\r','').replace('\n','') for info in detail.select('.e_hs12')][5:30]

    info = dict()
    for name, content in zip(item_names, item_content):
        info['url'] = page_url
        info[name] = content
    item_info.insert_one(info)

def get_rest_of_url():
    db_url = [item['url'] for item in urls_list.find()]
    if item_info.find():
        index_url = [item['url'] for item in item_info.find()]
    else:
        index_url = []
    x = set(db_url)
    y = set(index_url)
    rest_of_url = x - y
    return rest_of_url

if __name__=='__main__':
    url = 'http://newhouse.cnnbfdc.com/lpxx.aspx'
    pool = Pool()
    while len(get_rest_of_url()) != 0:
        pool.map(get_detail, get_rest_of_url())
