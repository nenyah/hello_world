#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-05-08 15:07:44
# @email: lucibriel@163.com
# @Last Modified by: Steven
# @Last Modified time: 2018-03-24 15:27:03

import requests
from bs4 import BeautifulSoup
import pymongo
from multiprocessing import Pool
import time
# from crawler_tool import request
import arrow

client = pymongo.MongoClient('localhost', 27017)
fangcan = client['fangcan']
urls_list = fangcan['urls_list']
item_info = fangcan['item_info']

PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def get_list_url(url):
    data = []
    proxies = {
        "http": 'http://' + get_proxy(),
    }
    print(proxies)
    web = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(web.text, 'lxml')
    print(soup.prettify())
    print(soup.select('.PagerCss a'))
    # max_page = soup.select('.PagerCss a')[-1]['href'].split('=')[-1]

    # for page in range(1, int(max_page) + 1):
    #     list_url = 'http://newhouse.cnnbfdc.com/lpxx.aspx?p={0}'.format(
    #         str(page))
    #     html = request.get(list_url, 3)
    #     soup = BeautifulSoup(html.text, 'lxml')
    #     all_a = soup.select(".sp_zi12c")
    #     for a in all_a:
    #         title = a.text.strip()
    #         href = 'http://newhouse.cnnbfdc.com/' + a['href']
    #         info = {'name': title, 'url': href}
    #         print('Get list info: {0}'.format(info))
    #         if not urls_list.find({'url': info['url']}):
    #             urls_list.insert_one(info)


def tidy_content(content):
    return content.strip().replace(' ', '').replace(
        '\r', '').replace('\n', '').replace('\xa0地图定位', '').replace('：', '')


def get_detail(page_url):
    proxies = {
        "http": 'http://' + get_proxy(),
    }
    html = requests.get(page_url, proxies=proxies)
    detail = BeautifulSoup(html.text, 'lxml')
    item_names = [tidy_content(info.text)
                  for info in detail.select('.sp_f12')][:29]
    if '地图定位' in item_names:
        item_names.remove('地图定位')
    item_content = [tidy_content(info.text)
                    for info in detail.select('td.e_hs12')][2:30]
    # print(item_names, len(item_names))
    # print(item_content, len(item_content))
    info = dict()
    for name, content in zip(item_names, item_content):
        info['date'] = arrow.now().format(f"YYYY-MM-DD")
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


if __name__ == '__main__':
    url = 'http://newhouse.cnnbfdc.com/lpxx.aspx'
    get_list_url(url)
    # pool = Pool()
    # while len(get_rest_of_url()) != 0:
    #     pool.map(get_detail, get_rest_of_url())
