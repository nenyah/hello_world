from selenium import webdriver
import time

url = 'http://www.aliexpress.com/wholesale?SearchText=men%27s+shoes'
driver = webdriver.PhantomJS()
driver.get(url)
time.sleep(5)
data = driver.find_elements_by_css_selector('a.product')
# print(data)
# print(type(data[0].text),data[0].text)
titles = [title.text for title in data]
print(titles)
print(len(titles))