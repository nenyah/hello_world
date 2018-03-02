# -*- coding: utf-8 -*-
# @Author: Steven
# @Date:   2018-01-15 13:02:00
# @Last Modified by:   Steven
# @Last Modified time: 2018-02-24 14:41:16
'''
# 总产品列表
https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&dateType=7&cateId=&productId=&cateLevel=&isValid=ALL&indexRule=&countryCode=TOTAL&iName=productAnalysisProductListExcel
# 单个产品信息
https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&productId=32598355504&gmvLevel=3&leafCate=200000970&startDate=2017-10-01&endDate=2018-01-13&indexList=payAmt&platformName=TOTAL&countryCode=TOTAL&compareType=0&iName=productAnalysisIndexInfoExcel'''

import requests
from bs4 import BeautifulSoup
import os
import time
from fake_useragent import UserAgent
import json

ua = UserAgent()
url = r"https://bp.aliexpress.com/manager/asyGetKeywordList.do?ctoken=ayrtl6oe58hy"

Cookie = 'ali_apache_id=10.181.239.59.1513657984416.179605.8; cna=aYS/EtPqGEsCAXxZhedTGB+9; ali_beacon_id=10.181.239.59.1513657984416.179605.8; aep_common_f=Gxln6xTjLymojKW7t7RsDc2VWGmzHYQ99pHpuE2CnDXJU6VUfFnlHg==; _ga=GA1.2.1320508373.1513658028; UM_distinctid=1606d15adaf1c2-005bfe6fc95a07-e323462-13c680-1606d15adb0b0a; __utmz=3375712.1515227606.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_uid=1515374152597757824; _seller_new_home=true; _gid=GA1.2.399778395.1517905681; __utma=3375712.1320508373.1513658028.1515566714.1518050832.3; __utmc=3375712; _hvn_login=13; xman_us_t=x_lid=cn1001787010&sign=y&x_user=3wZpDGrbdDsdfwxz+Z68ReYGUalFy1JwhkWB1N8DkOU=&ctoken=ayrtl6oe58hy&need_popup=y&l_source=aliexpress; xman_f=fjEIy3Tzw5DknPSHfY/XfUQaEsgG/zKpf0kLtWC7BufcIHrLp5IMdZhucfuYs3nY4cofzBWPnPt25zziaHCdHuKL+w/J+w96r+zWLRHuyNE98orJI5u/wtCK3VaNDAmScvldKYX0eOQyOe5Ak2G6twz8hvKE17nrQdTM5jSptfhCrdvwh7HYgh/pYUD2qqlcOLzJP35sKQuun6Mglaq3cNnJK3/e2H12RO8nifmjXvfszkKnfwU3uxYy14syx6E8Fzi/GiBmATzBKGQK2Z+XSDqG0moGa9SiO8PyMzzwdAVxkbShh8ZkBvV/E7HXYv7VPyl9yaovJ36zHsIq6nslcaIEgdLYNl+YYmwnpjT8dCB0GWXDJRT71JJZm1lrYY84E7fXna0+9otpCtVyvDsne6TdAKM8SNL6vetuW/bVXRw=; acs_usuc_t=acs_rt=3984cb56999740f3b08dc92f8c17ad8e&x_csrf=1dv84g500zv3j; ali_apache_track=mt=2|ms=|mid=cn1001787010; ali_apache_tracktmp=W_signed=Y; intl_locale=zh_CN; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091523308041%0932712557247%0932754389984%0932713279253%0932584744141%0932598355504%0932757455655%0932831586051; translate=en; xman_us_f=x_l=1&x_locale=zh_CN&no_popup_today=n&x_user=CN|Steven|Tan|cnfm|202367604&zero_order=y&last_popup_time=1513658026348; aep_usuc_f=site=glo&region=US&b_locale=en_US&iss=y&s_locale=zh_CN&isfm=y&c_tp=USD&x_alimid=202367604; JSESSIONID=7244D19CF5220252553B70B008E6417F; xman_t=chw2Qe5/Dew0JR6ezdXqH9mBtW1hdHnQIy8kS0uOUc1+96yiRZkuYyVB1WmxTBT4XeE2izr8SLQRSAkXA/6I6iwwiR4ZPoWmohgExMYjgXiVpUADw4bSDpbJYK4RVvljG19d52zqmzU8U8UB/xyId6P6xi3I2Qzl5oWBQCHMpBJbAnaK0Przm5c/xbxkenySFpkYY5pEf4kBkOg5lLNFEb8tXmtu+2JivFyis1QiYClZD9LXMhBw1QfHR8aOqxgPmTED7fBuNiPu/ZPAZrpG+hy2oiVJzq5m5zGi6emO5ip/gehgelm2ErbUM9ToJDzdFTLtXncVL9zXsS3RnWCsgI7yEbn6gcaakoZbXhukyICHnl0zIXseR+qYYqvyNZVhy0eb9lfj1QMSIukEW+YQTO1oMg+Sm/Q1daj761vy2KcIIocUdrbgrcW8L2PodPcfKUWJgujTEhQH8K9H4kO54PNz+1DOcwLW52WUCnkluDFV1hLjqGYRd3kEz4LpxrWLEktVQuaFB8MMI2a30rucgsnbS/kxYVNp0fnfQLtpDzZ21em1eMhCWemmw25SctiYD5U2Bb8fZBMWCo52Jz2URQV+l1R7HXAjxtIlZssKWmlwk1dTGgjYt2MK/IuOpA/GRL3aGr9j1h6wfefzOos2Xi4JENREef8ZKB984O1EGU4=; intl_common_forever=WNp1tJ6qhulz+sgDB15l/8BDiDl0rbJRePL+BD6ueYL3ogsbpM/tCw==; isg=BCUlE1Dfk181V_dAATBCNhPsNOGfytiFyRu9CScK39xrPkaw77EGxouYzKJIPvGs'

headers = {
    'User-Agent': ua.random,
    'Cookie': Cookie,
    'referer':'https://bp.aliexpress.com/manager/focus_keyword_list.htm?campaignId=75490100939&unitId=466001503'
}

postData = {'json': json.dumps({"dateRange": 7, "campaignId": "75490100939", "unitId": "466001503", "currentPage": 1, "keyword": "", "typeOrder": "cpc", "order": "DESC"}),
            '_csrf_token_': '1dv84g500zv3j',
            '_dt_page_id_': 'aysetpqgescaxxzh161730262984b1513f07c0ec0f'
            }

ali_s = requests.Session()

web = ali_s.post(url,
                 data=postData,
                 headers=headers)

keyword_data = web.json()['data']
for info in keyword_data:
    key_id = info['id']
    print(key_id, type(key_id), info['word'])

    ModifyData = {'json': json.dumps({"keywordId": key_id, "price": 1.5}),
                  '_csrf_token_': '1dv84g500zv3j',
                  '_dt_page_id_': 'aysetpqgescaxxzh161730262984b1513f07c0ec0f'
                  }
    web = ali_s.post(url,
                     data=postData,
                     headers=headers)
    print(web.json()['status'])

# file = r"F:\Work\06-Work\Data Anlysis\08-流量来源分析\产品流量"
# if os.path.exists(file):
#     os.chdir(file)
# else:
#     os.makedirs(file)


# def main():
#     menu = get_menu(path)
#     for id in menu:
#         content = get_content(id)
#         save_to_csv(content)


# def get_menu(path):
#     pass


# def build_content_url(content_data):
#     # url =
#     # f"https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&productId={id}&gmvLevel=3&leafCate=200000970&startDate=2017-10-01&endDate=2018-01-13&indexList=payAmt&platformName=TOTAL&countryCode=TOTAL&compareType=0&iName=productAnalysisIndexInfoExcel"
#     print(productId)
#     return url


# id = '32598355504'
# content_data = {
#     'productId': id,
#     'gmvLevel': 3,
#     'leafCate': 200000970,
#     'startDate': '2018-01-07',
#     'endDate': '2018-01-13',
#     'indexList': 'payAmt',
#     'platformName': 'TOTAL',
#     'countryCode': 'TOTAL',
#     'compareType': 0
# }


# def get_content(url, data=None):
#     try:
#         download = requests.get(url, headers=headers, data=data)
#         print(download.status_code)
#         content = download.content
#         print(len(content))
#     except:
#         print(url, "Error")
#     # print(content)
#     return content


# def save_to_csv(content, filename=None):
#     with open(filename, 'wb') as f:
#         f.write(content)


# def test():
#     # url = "https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&iName=productAnalysisIndexInfo"
#     # content = get_content(url, content_data)
#     # save_to_csv(content, "test.xls")
#     build_content_url(content_data)


# if __name__ == '__main__':
#     test()
