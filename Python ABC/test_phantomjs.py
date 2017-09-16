#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,re
from bs4 import BeautifulSoup

def tidy(str):
	return re.sub("\t|\n","",str)

def getReview(productId):
	memberId = "202367604"
	url = 'https://feedback.aliexpress.com/display/productEvaluation.htm?productId={0}&ownerMemberId={1}'.format(productId, memberId)
	obj = webdriver.PhantomJS()
	obj.set_page_load_timeout(5)
	html = ""
	try:
		obj.get(url)
		time.sleep(5)
		data = []
		maxs = obj.find_elements_by_css_selector("a.ui-goto-page")
		maxPage = [m.text for m in maxs][-2]
		print("总页数：{0}".format(maxPage))
		for i in range(1, int(maxPage)+2):
			print("第{0}页".format(str(i)))
			soup = BeautifulSoup(obj.page_source,'lxml')
			div = soup.find_all(class_="feedback-item")
			for tag in div:
				username = tag.find(class_="user-name").text
				country = tag.find(class_="css_flag").text
				order_info = tag.find(class_="user-order-info").text
				order_info = tidy(order_info)
				feedback = tag.find(class_="f-content").text
				isImg = tag.find_all("img")
				img = [img.get("src") for img in isImg] if isImg else None
				print(username,country,order_info,img)
			# obj.save_screenshot("{}-{}.png".format(productId,str(i)))
			if i == 20: break
			nextpage = obj.find_element_by_css_selector("a.ui-pagination-next")
			nextpage.click()
		# feedbacks = set(feedbacks)
		with open("review.html","a", encoding="utf-8") as f:
			f.write(html)

	except Exception as e:
		print(e)


if __name__ == '__main__':
	productId = "32238331771"
	getReview(productId)
