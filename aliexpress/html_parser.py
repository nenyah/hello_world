# -*- coding: utf-8 -*-
# Created on 2018年3月9日
# @author: Administrator
import re


from bs4 import BeautifulSoup


class HtmlParser(object):

    def _get_new_data(self, page_url, soup):
        items = soup.find_all("li", "item")
        datas = []
        for item in items:
            title = item.find("h3").find("a").get("title").strip()  # 标题
            product_url = item.find("h3").find("a").get("href")
            price = item.find("div", "cost").find('b').text  # 价格
            order = item.find("div", "recent-order")
            order = int(re.findall(r"(\d+)", order.text)[0]) if order else 0
            discount = item.find("div", "img").find("div", "discount")
            discount = int(discount.find("span").text) if discount else 0

            data = {
                'page_url': page_url,
                'title': title,
                'price': price,
                'order': order,
                'product_url': product_url,
                'discount': discount
            }
            datas.append(data)
        return datas

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # <a href="//naturalhome.aliexpress.com/store/518251/search/2.html?spm=2114.12010615.0.0.6724294a2uPEHf&amp;origin=n&amp;SortType=bestmatch_sort" data-mango="true" data-spm-anchor-id="2114.12010615.0.0">2</a>
        links = soup.find_all('a', href=re.compile(r".*/search/\d+\.html.*"))
        for link in links:
            new_url = link['href'].split("?")[0]
            new_full_url = 'https:' + new_url
            new_urls.add(new_full_url)
        return new_urls

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'lxml')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
