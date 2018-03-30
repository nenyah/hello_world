# -*- coding: utf-8 -*-
# @Author: nenyah
# @Date:   2017-08-01 21:38:46
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-29 17:05:47 

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.baidu.com")

driver.find_element_by_id("kw").send_keys("Selenium2")
driver.find_element_by_id("su").click()
