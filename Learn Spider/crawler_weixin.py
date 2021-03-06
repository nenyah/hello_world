# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-03-04 14:43:55
# @Last Modified by:   Steven
# @Last Modified time: 2018-03-06 15:30:13
"""
Function:
获取指定地址文章
Version:    2016-09-03
Author:     Steven
Contact:    lucibriel (at) 163.com
"""

import logging
import os
import re
import time
import sys

try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import pdfkit
import requests
from bs4 import BeautifulSoup
from lxml import etree
from crawler_tool import request

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""
file = r"./pdf/"

log = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter

log.addHandler(file_handler)
log.addHandler(console_handler)

log.setLevel(logging.INFO)


def check_exist(url, path=file):
    name = url.split('/')[-2] + '.jpg'
    return not (name in os.listdir(path))


class Crawler:
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, name, start_url):
        """
        初始化
        :param name: 将要被保存为PDF的文件名称
        :param start_url: 爬虫入口URL
        """
        self.name = name
        self.start_url = start_url

    @staticmethod
    def request(url, **kwargs):
        """
        网络请求,返回response对象
        :return:
        """
        response = request.get(url, 10, **kwargs)
        return response

    def parse_menu(self, response):
        """
        从response中解析出所有目录的URL链接
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError

    def run(self):
        start = time.time()
        options = {
            'page-size': 'Letter',
            'image-dpi': 1500,
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        htmls = []
        for index, url in enumerate(self.parse_menu(self.request(self.start_url))):
            log.info(url)
            html = self.parse_body(self.request(url))

            f_name = ".".join([str(index), "html"])
            with open(file + f_name, 'wb') as f:
                f.write(html)
            htmls.append(file + f_name)
        try:
            config = pdfkit.configuration(
                wkhtmltopdf=r"D:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe")
            pdfkit.from_file(htmls, self.name + ".pdf",
                             options=options, configuration=config)
        except:
            log.error("生成错误", exc_info=True)
        for html in htmls:
            os.remove(html)
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)


class SaleCrawler(Crawler):
    """
    亚马逊运营
    """

    def download_pic(self, url):
        name = url.split('/')[-2] + '.jpg'
        with open(file + name, "wb") as f:
            f.write(requests.get(url).content)

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        tree = etree.HTML(response.text)
        menu_tag = tree.xpath('//div[@id="js_content"]//a/@href')
        for url in menu_tag:
            yield url

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(response.content, 'lxml')
            body = soup.find_all(id="img-content")[0]
            body.find_all("img")[-2].decompose()

            # 加入标题, 居中显示
            title = body.h2
            title.name = "h1"
            title.wrap(soup.new_tag("center"))
            profile_container = body.find('div', class_="profile_container")

            del profile_container['style']

            html = str(body)
            p1 = re.compile(r'<img.*?"(http:\S+)"(?:\s[^>]*)>', re.S)
            p2 = re.compile(
                r'<script[^>]*?>[\s\S]*?"(http:\S+)"[\s\S]*?<\/script>', re.S)

            def build_img(m):
                return '<center><img src="' + './' + m.group(1).split('/')[-2] + '.jpg' + '" style="max-width=650px;" /></center>'
            for href in p2.findall(response.text):
                if 'mmbiz' in href and check_exist(href):
                    print(href)
                    self.download_pic(href)
            for href in p1.findall(response.text):
                if 'mmbiz' in href and check_exist(href):
                    print(href)
                    self.download_pic(href)
            html = p1.sub(build_img, html)
            html = p2.sub(build_img, html)
            html = html_template.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            log.error("解析错误", exc_info=True)


if __name__ == '__main__':
    start_url = r"https://mp.weixin.qq.com/s?__biz=MzA4ODY4ODUzNQ==&mid=2663450782&idx=1&sn=30b5160e66c0671df13c8436f6f2ce5f"
    crawler = SaleCrawler("顾小北", start_url)
    crawler.run()
