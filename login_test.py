#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
登录demo
Version:    2016-09-03
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import requests
from bs4 import BeautifulSoup
import re
i = 0
postData = {"start": i} 
url = 'https://book.douban.com/top250'
geturl = url + "?start=" + str(i)                     #要获取的页面地址
print("Now to get " + geturl)
postData = {"start":i}                                #post数据
header = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
s = requests.Session()
res = s.post(geturl,data = postData,headers = header)    #post
# print(res.text)
soup = BeautifulSoup(res.text,"lxml")       #BeautifulSoup解析
# titles = [i.text.strip() for i in soup.select('.pl2 a')]
table = soup.findAll('table',{"width":"100%"})        #找到所有图书信息的table
# print(table)
# print(titles)
sz = len(table)                                       #sz = 25,每页列出25篇文章
for j in range(1,sz+1):                               #j = 1~25
    sp = BeautifulSoup(str(table[j-1]),"lxml") #解析每本图书的信息
    # print(sp.div)
    imageurl = sp.img['src']                          #找图片链接
    bookurl = sp.a['href']                            #找图书链接
    bookName = sp.div.a['title']
    nickname = sp.div.span                            #找别名
    if(nickname):                                     #如果有别名则存储别名否则存’无‘
        nickname = nickname.string.strip()
    else:
        nickname = "None"
     
    print(type(imageurl),imageurl)
    print(type(bookurl),bookurl)
    print(type(bookName),bookName)
    print(type(nickname),nickname)
     
    notion = str(sp.find('p',{"class":"pl"}).string)   #抓取出版信息,注意里面的.string还不是真的str类型
    #print(type(notion),notion)
    rating = str(sp.find('span',{"class":"rating_nums"}).string)    #抓取平分数据
    nums = sp.find('span',{"class":"pl"}).string                    #抓取评分人数
    nums = nums.replace('(','').replace(')','').replace('\n','').strip()
    nums = re.findall('(\d+)人评价',nums)[0]
    print(type(rating),rating)
    print(type(nums),nums)
    # download_img(imageurl,bookName)                     #下载图片
    # book = requests.get(bookurl)                        #打开该图书的网页
    # sp3 = BeautifulSoup(book.content,"html.parser")     #解析
    # taglist = sp3.find_all('a',{"class":"  tag"})       #找标签信息
    # tag = ""
    # lis = []
    # for tagurl in taglist:
    #     sp4 = BeautifulSoup(str(tagurl),"html.parser")  #解析每个标签
    #     lis.append(str(sp4.a.string))
     
    # tag = ','.join(lis)        #加逗号
    # if tag == "":              #如果标签为空，置"无"
    #     tag = "None"
