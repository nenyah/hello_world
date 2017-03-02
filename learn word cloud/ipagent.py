import requests
from bs4 import BeautifulSoup
import random
import re
from multiprocessing import Pool



USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

headers = {
	'User-Agent':random.choice(USER_AGENTS)
}
def isExsitIP():
	path = r'C:\Users\steve\Desktop\ips_valid.txt'
	if os.path.exists(path):
		with open(r'C:\Users\steve\Desktop\ips_valid.txt','r') as f:
			PROXIES = f.read().split('\n')
		proxies = {
			'http': random.choice(PROXIES)
		}
		return True
	return False

IP_POOL = []

# 获取最大页码
def getMaxPage():
	url = 'http://www.xicidaili.com/nn/'
	r = requests.get(url, headers=headers).text
	soup = BeautifulSoup(r, 'lxml')
	max_page = soup.find('div','pagination').text.split()[-3]
	return int(max_page)


# 检验IP
def checkIP(ip):
	# 检验地址:
	check_url = "http://ip.chinaz.com/getip.aspx"
	proxies={'http':ip}
	print('CHCEK: {}'.format(proxies))
	try:
		r = requests.get(
			check_url, 
			headers=headers, 
			proxies=proxies, 
			timeout = 5
			)
		r.raise_for_status()
	except requests.RequestException as e:
		print(e)
	else:
		if r.status_code == 200:
			print('{} is valid.'.format(ip))
			with open('ips_valid.txt','a+') as f:
				f.write(ip+'\n')
			return True
	return False


# 获取IP
def getIP(url):
	if isExsitIP():
		r = requests.get(url, headers=headers, proxies=proxies).text
	else:
		r = requests.get(url, headers=headers).text
	soup = BeautifulSoup(r, 'lxml')
	isExist = True if soup.find('tr', class_='odd') else False
	ips = soup.find_all('tr')
	if isExist:
		for x in range(1,len(ips)):
			ip = ips[x]
			tds = ip.find_all("td")
			# print(tds[1].contents[0])
			ip_temp = tds[5].string.lower()+'://'+tds[1].string+":"+tds[2].string
			print('GET {}'.format(ip_temp))
			# 检验IP
			if checkIP(ip_temp):
				IP_POOL.append(ip_temp)

	# return ip_pool




if __name__=="__main__":
	urls = ['http://www.xicidaili.com/nn/{}'.format(str(i)) 
		for i in range(1,getMaxPage())]
	p = Pool(4)
	for i in urls:
		p.apply_async(getIP, args=(i,))
	print('>>> Start to get IP...')
	p.close()
	p.join()
	print('>>> ALL IP get success.')
