# -*- coding: utf-8 -*-
# @Author: Steven
# @Date: 2018-03-10 10:29:02
# @Last Modified by: Steven
# @Last Modified time: 2018-03-10 12:49:04
# @file: spider_main.py

import url_manager, html_downloader, html_outputer, html_parser


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print(f"craw {count} : {new_url}")
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                count += 1
            except Exception as e:
                print("craw failed", e)
        self.outputer.output_csv()


if __name__ == '__main__':
    root_url = r"https://naturalhome.aliexpress.com/store/all-wholesale-products/518251.html"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
