#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
获取代理IP
Version:    2016-07-22
Author:     Steven
Contact:    lucibriel (at) 163.com
"""

import requests
from bs4 import BeautifulSoup
import asyncio


class SpiderProxy(object):
    """从http://www.xicidaili.com/wt 取代理ip"""
    headers = {
        "Host": "www.xicidaili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.xicidaili.com/wt/1",
    }

    def __init__(self, session_url):
        self.req = requests.session()
        self.req.get(session_url)

    def get_pagesource(self, url):
        '''取得html pagesource'''
        html = self.req.get(url, headers=self.headers)
        return html.content

    def get_all_proxy(self, url, n):
        ''' 取得所有1-n页上的代理IP'''
        data = []
        for i in range(1, n):
            html = self.get_pagesource(url + str(i))
            soup = BeautifulSoup(html, "lxml")

            table = soup.find('table', id="ip_list")
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                tmp = []
                for item in cells:

                    tmp.append(item.find(text=True))
                try:
                    tmp2 = tmp[1:2][0]
                    tmp3 = tmp[2:3][0]
                    tmp4 = tmp[5:6][0]
                    data.append({tmp4: tmp2 + ":" + tmp3})
                except Exception as e:
                    pass
        return data


class IsActivePorxyIP(object):
    """类组合
     用gevent 异步并发验证 代理IP是不是可以用
    """

    def __init__(self, session_url):
        self.proxy = SpiderProxy(session_url)
        self.is_active_proxy_ip = []

    def probe_proxy_ip(self, proxy_ip):
        """代理检测"""
        proxies = proxy_ip
        # print(proxies)
        s = requests.Session()
        try:
            html = s.get('http://1212.ip138.com/ic.asp', proxies=proxies)
            # print(html.text)
            if html:
                self.is_active_proxy_ip.append(proxy_ip)
                return True
            else:
                return False
        except Exception as e:
            return False
if __name__ == '__main__':
    session_url = 'http://www.xicidaili.com/wt/1'
    url = 'http://www.xicidaili.com/wt/'

    p_isactive = IsActivePorxyIP(session_url)
    proxy_ip_lst = p_isactive.proxy.get_all_proxy(url, 5)
    print(len(proxy_ip_lst))
    # 异步并发
    loop = asyncio.get_event_loop()
    tasks = [p_isactive.probe_proxy_ip(proxy_ip) for proxy_ip in proxy_ip_lst]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print(len(p_isactive.is_active_proxy_ip))