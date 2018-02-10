#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
# from crawler_tool import requests
import requests
import time
import re
from bs4 import BeautifulSoup
import arrow

end_page = 4
paths = (r"https://naturalhome.aliexpress.com/store/518251/search/{0}.html".format(str(i))
         for i in range(1, end_page + 1))

today = arrow.now().format("YY-MM-DD")

headers = {
    'User-Agent': "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
}


def get_html(path):
    try:
        reps = requests.get(path, headers=headers)
        time.sleep(5)
        print(reps.status_code)
        print("Begin to cralw: {}".format(path))
        return reps
    except Exception as e:
        raise e


def parse_html(content):
    soup = BeautifulSoup(content.text, 'lxml')
    # print(soup)
    ul = soup.find("ul", class_="items-list")
    item = ul.find_all('li', class_="item")
    print(len(item))
    for info in item:
        check_h3 = True if info.find('h3') else False
        check_discount = True if info.find(class_="discount") else False
        print(check_h3)
        if check_h3:
            p_url = info.h3.a.get("href")
            pid = p_url.split("_")[-1].split(".")[0]
            discount = info.find(class_="discount").text.strip(
            ) if check_discount else None
            print(pid, discount)
            yield (pid, discount)


def save_data(path):
    reps = get_html(path)
    with open(today + "-discount.txt", "a") as file:
        for pid, discount in parse_html(reps):
            file.write(f"{pid},{discount}\n")


def test():
    for path in paths:
        print(path)
        save_data(path)


if __name__ == '__main__':
    test()
