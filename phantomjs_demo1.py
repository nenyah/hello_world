from selenium import webdriver
from selenium.webdriver.common.keys import Keys
obj = webdriver.PhantomJS()
obj.set_page_load_timeout(25)
try:
    obj.get('http://www.baidu.com')
    obj.find_element_by_id('kw').send_keys(Keys.TAB)   #用于清除输入框的内容,相当于clear()
    obj.find_element_by_id('kw').send_keys('Hello')   #在输入框内输入Hello
    obj.find_element_by_id('su').send_keys(Keys.ENTER) #通过定位按钮，通过enter（回车）代替click()
    obj.save_screenshot("1.png")
    obj.quit()
except Exception as e:
    print(e)