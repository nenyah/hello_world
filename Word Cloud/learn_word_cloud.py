# coding:utf-8
__author__ = 'Steven Tan'

import jieba
import requests
import time
from bs4 import BeautifulSoup
# from multiprocessing import Pool

url = 'http://www.xieyixs.com/xy2408/'


headers = {
    'USER_AGENTS': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
}


def get_urls(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    dd = soup.find_all('dd')
    for i in range(len(dd)):
        a = dd[i].find('a')['href']
        full_url = 'http://www.xieyixs.com' + a
        # print(full_url)
        yield full_url


# url = 'http://www.xieyixs.com/xy2408/3658793.html'


def get_content(url):
    time.sleep(3)
    print("Try to get content from: {}".format(url))
    try:
        response = requests.get(url, headers=headers)
    except:
        print("Error: {}".format(url))
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('p', 'pdp').text
    return content


def save(content):
    with open(r'content.txt', 'a+', encoding="utf-8") as f:
        f.write(content)

if __name__ == '__main__':
    # p = Pool(4)
    url = 'http://www.xieyixs.com/xy2408/'
    for url in get_urls(url):
        save(get_content(url))
