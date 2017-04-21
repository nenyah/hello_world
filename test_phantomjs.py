#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def getReview(productId):
	memberId = "202367604"
	url = 'https://feedback.aliexpress.com/display/productEvaluation.htm?productId={}&ownerMemberId={}'.format(productId, memberId)
	obj = webdriver.PhantomJS()
	obj.set_page_load_timeout(5)
	try:
		obj.get(url)
		time.sleep(5)
		feedbacks = []
		maxs = obj.find_elements_by_css_selector("a.ui-goto-page")
		maxPage = [m.text for m in maxs][-2]
		print(maxPage)
		for i in range(1, int(maxPage)):
			data = obj.find_elements_by_css_selector('dt.buyer-feedback')
			feedbacks += [feedback.text for feedback in data]
			print(len(feedbacks))
			# obj.save_screenshot("{}-{}.png".format(productId,str(i)))
			nextpage = obj.find_element_by_css_selector("a.ui-pagination-next")
			nextpage.click()
		feedbacks = set(feedbacks)
		with open("{} feedback.txt".format(productId),"a", encoding="utf-8") as f:
			f.write('\n'.join(feedbacks))
	except Exception as e:
		print(e)

if __name__ == '__main__':
	productId = "32595316747"
	getReview(productId)
