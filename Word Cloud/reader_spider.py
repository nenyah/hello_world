# coding:utf-8
__author__ = 'Steven Tan'


from crawler_tool import request
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool
import os


class ReaderSpider:
    """docstring for ReaderSpider"""

    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.site = 'http://' + self.url.split('/')[2]
        self.count = 0
        self.menu = []

    def get_menu(self):
        temp = []
        response = request.get(self.url, 3)
        soup = BeautifulSoup(response.text, 'lxml')
        dd = soup.find_all('dd')
        for i in range(len(dd)):
            a = dd[i].find('a')['href']
            full_url = '{0}{1}'.format(self.site, a)
            temp.append(full_url)
        return temp

    def get_content(self, url):
        time.sleep(3)
        try:
            response = request.get(url, 3)
        except:
            print(f"{url} Error")
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1').text.strip()
        content = soup.find(id='content').text
        content = '\n'.join(content.split())
        self.save(content, title)

    def save(self, content, title):
        path = fr'E:\workspace\{self.title}'
        if os.path.exists(path):
            os.chdir(path)
        else:
            os.makedirs(path)
            os.chdir(path)

        print(title, 'Success')
        with open(title + '.txt', 'w', encoding="utf-8") as f:
            f.write(content)

    def run(self):
        start = time.time()
        self.menu = self.get_menu()
        p = Pool()
        for index, url in enumerate(self.menu):
            p.apply_async(self.get_content, (url, ))
        p.close()
        p.join()
        total_time = time.time() - start
        print(u"总共耗时：{0} 秒".format(total_time))


if __name__ == '__main__':
    url = 'http://www.xieyixs.com/xy2408/'
    rs = ReaderSpider(url, '儒道至圣')
    rs.run()
