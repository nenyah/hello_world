# -*- coding: utf-8 -*-
# @Author: Steven
# @Date:   2018-01-15 13:02:00
# @Last Modified by:   Steven
# @Last Modified time: 2018-01-17 10:01:01
'''
# 总产品列表
https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&dateType=7&cateId=&productId=&cateLevel=&isValid=ALL&indexRule=&countryCode=TOTAL&iName=productAnalysisProductListExcel
# 单个产品信息
https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&productId=32598355504&gmvLevel=3&leafCate=200000970&startDate=2017-10-01&endDate=2018-01-13&indexList=payAmt&platformName=TOTAL&countryCode=TOTAL&compareType=0&iName=productAnalysisIndexInfoExcel'''

import requests
from bs4 import BeautifulSoup
import os
import time

Cookie = 'ali_apache_id=10.181.239.59.1513657984416.179605.8; cna=aYS/EtPqGEsCAXxZhedTGB+9; ali_beacon_id=10.181.239.59.1513657984416.179605.8; aep_common_f=Gxln6xTjLymojKW7t7RsDc2VWGmzHYQ99pHpuE2CnDXJU6VUfFnlHg==; _ga=GA1.2.1320508373.1513658028; UM_distinctid=1606d15adaf1c2-005bfe6fc95a07-e323462-13c680-1606d15adb0b0a; __utmz=3375712.1515227606.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_uid=1515374152597757824; __utma=3375712.1320508373.1513658028.1515227606.1515566714.2; acs_usuc_t=acs_rt=7a80809a70254b819ce96492cd3dd0f4&x_csrf=ir2k_ebpreec; _gid=GA1.2.2057798738.1515977577; xman_us_t=x_lid=cn1001787010&sign=y&x_user=ggq+r87WzpEDKbj0/uiLe+Vk3molImEpNc9qeMTrb2M=&ctoken=tn1g3gdr18j5&need_popup=y; xman_f=MjS40SSNsC7ql5WzMhnhpfmZ6fWv4qCR56MBsT83X0LUuvTiGA519TDPyWiH4CDBlA5vn2RuGSfuJbNiTFDzdmWlxa/2LuSNoBQ0bBuwi8Xh3MifLvAsPhXrzMDtZo1MV8QoQw9XmkwELAWE1uJeOISdeb8yksq5CAaJMnQZ/0LaoiceC/G6FZVsGHs/hvx+DAExslptUNthZBKY1CDjXTYgfFLm20ZcwTEVeLnp+qxiAr+lNdcChPh35UDtF7xu0cqIkwHSEKWNJV0N5xvmtZv+s3jeZf7P+BbfSCmRx4tBYJAYnPGuHy8w0QwsGi44qWabFnb4BBUvgarR1Fed/phf+8PFfKFxEArsHp0aIyuvr2KxlSZXjnvAzWEZwStStQhGAdNUJx0wSmfHYFLp1qZDik0vzZt9Y+3hmTAxLY0=; _m_h5_c=8b74b068a6cadf4c436f7643cb43dc3e_1515994215216%3Bfc7d6f3cccdc3a85e079f7be4195a076; intl_locale=zh_CN; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932598383431%091523308041%0932675003154%0932831586051%0932827796732%0932722171683%0932799633898%0932598355504; ali_apache_track=mt=2|ms=|mid=cn1001787010; ali_apache_tracktmp=W_signed=Y; xman_us_f=x_l=1&x_locale=zh_CN&no_popup_today=n&x_user=CN|Steven|Tan|cnfm|202367604&zero_order=y&last_popup_time=1513658026348; isg=Apubrv4ORX6gD7nu64J08GmeKv_F2K4Db8GSSI3YdxqxbLtOFUA_wrnuePuY; aep_usuc_f=region=US&site=glo&b_locale=en_US&iss=y&s_locale=zh_CN&isfm=y&x_alimid=202367604&c_tp=USD; xman_t=0AhVg4D7RSGF7KeCcF6KCi/TvSJkPCdOWP9jLzTaAi6HMKl8ABFtx0qvcKcRQNyTMJGzZiXDp0GObur7WNIdIDPwIH5VW/kXZh6qkZD+N/2XLkdldetVAed77gh1UwozJMn3I5OZ6LuJe0a/ye4jeXIiEFnegTvNd4NPWExS/2T1VOyKYShXq9jglkny78c9V0h4XNIbQFYc8SUArbFJSJhLYClMjRB6ybDUgqzQuW+/UQyPFL/3dgMRs8O1Xhs2EHHXycDaUPJ910jAW6vxuierT+Xxv0a/wLUDoAE2wnHN5ACwe0h4g9h1fWRlbcb5eG+iLJ7lFDZAfrMPf52vpJG+6DZkea2N280S4O3Upn8aHs2v5Q+43llelROxp7LXMqsAlVwZCjB3gjPvojfgCZu0sS1KNXoc0pDi6bF1XmCxCfgKkDapP0AawZn+GWZRR077ugVa8nTbmNqF2aTBShX4rnQcUfEd9nSnD9aCwOOKQdFkkI6H3Fd6VUXuf8+x5xaG6nCAD9VHVTrj0oNcrhgfUS5N5fZ+X20yi3vykpTyllezd+N6HEEM57Vp+cS0f+Wv6YTZFwhJgwk0M/SzXX0NArAgl9TjgifoqJ3C1uuvpUWvXcPdnG+4R1P8O099H+ukaICKHtHxQLHTPtw8Sr+WMNaoIk2p; intl_common_forever=FTKsrQsgMkJXashsdhDp0IY8hPjbeZy1NnerygIz5C7UOY5thmrUXg=='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Cookie': Cookie
}

file = r"F:\Work\06-Work\Data Anlysis\08-流量来源分析\产品流量"
if os.path.exists(file):
    os.chdir(file)
else:
    os.makedirs(file)


def main():
    menu = get_menu(path)
    for id in menu:
        content = get_content(id)
        save_to_csv(content)


def get_menu(path):
    pass

def build_content_url(content_data):
# url =
# f"https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&productId={id}&gmvLevel=3&leafCate=200000970&startDate=2017-10-01&endDate=2018-01-13&indexList=payAmt&platformName=TOTAL&countryCode=TOTAL&compareType=0&iName=productAnalysisIndexInfoExcel"
	print(productId)
	return url
id = '32598355504'
content_data = {
    'productId': id,
    'gmvLevel': 3,
    'leafCate': 200000970,
    'startDate': '2018-01-07',
    'endDate': '2018-01-13',
    'indexList': 'payAmt',
    'platformName': 'TOTAL',
    'countryCode': 'TOTAL',
    'compareType': 0
}


def get_content(url, data=None):
    try:
        download = requests.get(url, headers=headers, data=data)
        print(download.status_code)
        content = download.content
        print(len(content))
    except:
        print(url, "Error")
    # print(content)
    return content


def save_to_csv(content, filename=None):
    with open(filename, 'wb') as f:
        f.write(content)


def test():
    # url = "https://datamatrix.aliexpress.com/common/.dox?action=CommonAction2&iName=productAnalysisIndexInfo"
    # content = get_content(url, content_data)
    # save_to_csv(content, "test.xls")
    build_content_url(content_data)

if __name__ == '__main__':
    test()
