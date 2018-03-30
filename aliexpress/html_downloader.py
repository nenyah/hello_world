# -*- coding: utf-8 -*-
# @Author: Steven
# @Date: 2018-03-10 10:29:02
# @Last Modified by: Steven
# @Last Modified time: 2018-03-10 12:45:43
# @file: html_downloader.py

from ip_agent import request


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        resp = request.get(url, 15)
        if resp.status_code != 200:
            return None
        return resp.text
