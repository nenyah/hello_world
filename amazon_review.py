#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
获取amazon评价信息存入mongodb
Version:    2016-07-27
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import re
import requests
from bs4 import BeautifulSoup
import pymongo
import time


headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
client = pymongo.MongoClient('localhost', 27017)
amazon = client['amazon']
reviews = amazon['reviews']


def get_asin(url):
    return re.search(r'\/dp\/(.*)\/', url).group(1)


def get_review_page_number(asin):
    url = 'http://www.amazon.com/product-reviews/{0}'.format(asin)
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    href = soup.select('.a-last a')[0].get('href')
    max_page = re.search(r'pageNumber=(\d+)', href).group(1)
    return int(max_page)


def get_info(url, asin):
    time.sleep(1)
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    review_title = soup.select('#cm_cr-review_list .review-title')
    review_rating = soup.select('#cm_cr-review_list .review-rating span')
    review_date = soup.select('#cm_cr-review_list .review-date')
    review_text = soup.select('#cm_cr-review_list .review-text')
    for title, rating, date, text in zip(review_title, review_rating, review_date, review_text):
        data = {
            'title': title.text,
            'rating': float(rating.text.split()[0]),
            'date': date.text.split('on ')[-1],
            'text': text.text,
            'asin': asin
        }
        print(data)
        # reviews.insert_one(data)


def get_urls(url):
    asin = get_asin(url)
    max_page = get_review_page_number(asin)
    urls = ['http://www.amazon.com/product-reviews/{0}?pageNumber={1}'.format(asin, str(num)) for num in
            range(1, max_page + 1)]
    return urls

if __name__ == '__main__':
    url = 'https://www.amazon.com/ASICS-Gel-Nimbus-16-2E-Running/dp/B00ES82H6K/ref=sr_1_20?s=apparel&ie=UTF8'
    asin = get_asin(url)
    for url in get_urls(url):
        get_info(url, asin)
