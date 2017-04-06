#coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
url = r'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2016451525964'

user = {'email':'********','password':'*********'}
s = requests.Session()
r = s.post(url,data = user)
res = s.get('http://www.renren.com/231570634')

soup = BeautifulSoup(res.text,'lxml')
vists = soup.select('.headpichold a')
# print(soup)
visit = [v.get('title').split()[0] for v in vists]
print(*visit,sep='\n')

