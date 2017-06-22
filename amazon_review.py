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
import pandas as pd
# import pymongo
import time


headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
# client = pymongo.MongoClient('localhost', 27017)
# amazon = client['amazon']
# reviews = amazon['reviews']


def get_asin(url):
    return re.search(r'\/dp\/(.*)\/', url).group(1)


def get_review_page_number(asin):
    url = 'http://www.amazon.com/product-reviews/{0}'.format(asin)
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    href = soup.select(
        'div.a-section.a-spacing-medium .a-declarative a.a-size-base')[0].text
    comments = re.search(r'See all (\d+\,*\d+) reviews', href).group(1)
    max_page = int(''.join(comments.split(','))) // 10 + 1
    return max_page


def get_info(url, asinc):
    df = pd.DataFrame()
    time.sleep(1)
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    review_title = soup.select('#cm_cr-review_list .review-title')
    review_rating = soup.select('#cm_cr-review_list .review-rating span')
    review_date = soup.select('#cm_cr-review_list .review-date')
    review_text = soup.select('#cm_cr-review_list .review-text')
    size_and_clor = soup.select(
        '#cm_cr-review_list .a-size-mini.a-color-secondary')
    for title, rating, date, text, size_and_clor in zip(review_title, review_rating, review_date, review_text, size_and_clor):
        data = {
            'title': title.text,
            'rating': float(rating.text.split()[0]),
            'date': date.text.split('on ')[-1],
            'text': text.text,
            'size_and_color': size_and_clor.text,
            'asin': asin
        }
        df = df.append(data, ignore_index=True)
        # print(data)
        # reviews.insert_one(data)
    # print(df.info())
    return df


def get_urls(url):
    asin = get_asin(url)
    max_page = get_review_page_number(asin)
    print(max_page)
    urls = ['http://www.amazon.com/product-reviews/{0}?pageNumber={1}&reviewerType=all_reviews'.format(asin, str(num)) for num in
            range(1, max_page + 1)]
    return urls

if __name__ == '__main__':
    url = 'https://www.amazon.com/Capezio-Womens-DS11-Fierce-Sneaker/dp/B0009Z8B0M/'
    asin = get_asin(url)
    df = pd.DataFrame()
    for url in get_urls(url):
        df = df.append(get_info(url, asin), ignore_index=True)
    df.to_csv('{}.csv'.format(asin), index=False)
    print(df.info())
