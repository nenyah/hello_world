#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-03-04 14:43:55
# @email: lucibriel@163.com
# @Last Modified by:   Steven
# @Last Modified time: 2018-01-31 13:42:10
from bs4 import BeautifulSoup
import os
from crawler_tool import request  # 导入模块变了一下


class mzitu():

    def all_url(self, url):

        # 这儿更改了一下（是不是发现  self 没见了？）
        html = request.get(url, 3, refferer='http://www.mzitu.com/99566')
        all_a = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='all').find_all('a')[1:]
        for a in all_a:
            title = a.get_text()
            print('开始保存：', title)
            path = str(title).replace("?", '_').replace(':', '')
            self.mkdir(path)
            os.chdir("E:\mzitu\\" + path)
            href = a['href']
            self.html(href)

    def html(self, href):
        # 这儿更改了一下（是不是发现  self 没见了？）
        html = request.get(href, 3, refferer='http://www.mzitu.com/99566')
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[
            6].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self, page_url):
        # 这儿更改了一下（是不是发现  self 没见了？）
        img_html = request.get(
            page_url, 3, refferer='http://www.mzitu.com/99566')
        img_url = BeautifulSoup(img_html.text, 'lxml').find(
            'div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        name = img_url[-9:-4]
        print('开始保存：', img_url)
        # 这儿更改了一下（是不是发现  self 没见了？）
        img = request.get(img_url, 3, refferer='http://www.mzitu.com/99566')
        with open(name + '.jpg', 'wb') as f:
            f.write(img.content)

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("E:\mzitu", path))
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(os.path.join("E:\mzitu", path))
            return True
        else:
            print('名字叫做', path, '的文件夹已经存在了！')
            return False


if __name__ == '__main__':
    Mzitu = mzitu()  # 实例化
    # 给函数all_url传入参数  你可以当作启动爬虫（就是入口）
    Mzitu.all_url('http://www.mzitu.com/all')
