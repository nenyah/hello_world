#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
根据传入的产品编码查找相关信息
Version:    2016-09-03
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import re
import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Connection': 'keep-alive'
}


def find_sku(attr):
    return attr if re.search(r'EATGE.*', attr) and len(attr) > 9 else None


def get_sku(product_num):
    url = 'http://m.aliexpress.com/item-desc/{0}.html'.format(product_num)
    web_data = requests.get(url, headers=headers)
    # time.sleep(2)
    soup = BeautifulSoup(web_data.text, 'lxml')
    sku_exits = True if 'SKU' in [
        item.text for item in soup.select('.key')] else False
    if sku_exits:
        sku = filter(find_sku, [item.text for item in soup.select('.value')])
        print('{0}:{1}'.format(product_num, list(sku)[0]))
    else:
        print('{0} has no sku'.format(product_num))


if __name__ == '__main__':
    products_num = '''
    32601892116
    32600494782
    32600506780
    32600510647
    32600590188
    32600598133
    32600709587
    32613130885
    32613130901
    32613138725
    32614084166
    32614939905
    32614943873
    32614951801
    32614987496
    32622478208
    32622513423
    32624523708
    32624539402
    32624559061
    32600918392
    32602419796
    32602487966
    32602863413
    32604830730
    32604886329
    32604933804
    32604945763
    32605832619
    32605844454
    32605852403
    32605896108
    32607015414
    32607019395
    32607031284
    32612973847
    32613005718
    32613021558
    32600482919
    32600486906
    32600494774
    32600494775
    32600769173
    32601800476
    32601860516
    32601864433
    32602471621
    32602475597
    32602479553
    32602551181
    32602831608
    32602831622
    32602855394
    32602867335
    32600721427
    32600721902
    32600818297
    32600890588
    32600898526
    32600902479
    32600902491
    32600906424
    32600910435
    32600914371
    32600914393
    32600922310
    32600961406
    32600969355
    32601069544
    32601081395
    32601085398
    32601089365
    32601093163
    32601093165
    32601420690
    32601440483
    32601440955
    32601444926
    32601528383
    32601528387
    32601540268
    32601548197
    32601572081
    32601764719
    32601772518
    32601772523
    32601780477
    32645742125
    32647088532
    '''
    for num in products_num.split():
        get_sku(num)
