# -*- coding: utf-8 -*-
# @Author: nenyah
# @Date:   2017-08-01 21:38:46
# @Last Modified by:   nenyah
# @Last Modified time: 2017-08-02 21:00:35

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

driver.find_element_by_id("kw").send_keys("Selenium2")
driver.find_element_by_id("su").click()
