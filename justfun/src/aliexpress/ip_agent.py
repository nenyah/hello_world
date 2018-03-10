# -*- coding: utf-8 -*-
# Created on 2018年3月10日
# @author: Administrator

import random
import re
import time

from fake_useragent import UserAgent
import requests


class download():

    def __init__(self):

        self.iplist = []  # 初始化一个list用来存放我们获取到的IP
        html = requests.get("http://www.xicidaili.com/nn/")  # 不解释咯
        # 表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！

        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)
        for ip in iplistn:
            i = re.sub('\n', '', ip)  # re.sub 是re模块替换的方法，这儿表示将\n替换为空
            self.iplist.append(i.strip())  # 添加到我们上面初始化的list里面

    def get(self, url, timeout, proxy=None, num_retries=6):  # 给函数一个默认参数proxy为空
        # 从self.user_agent_list中随机取出一个字符串
        ua = UserAgent()
        # 构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
        headers = {'User-Agent': ua.random}

        if proxy is None:  # 当代理为空时，不使用代理获取response（别忘了response啥哦！之前说过了！！）
            try:
                # 这样服务器就会以为我们是真的浏览器了
                return requests.get(url, headers=headers, timeout=timeout)
            except:  # 如过上面的代码执行报错则执行下面的代码

                if num_retries > 0:  # num_retries是我们限定的重试次数
                    time.sleep(10)  # 延迟十秒
                    print('获取网页出错，10S后将获取倒数第：', num_retries, '次')
                    # 调用自身 并将次数减1
                    return self.get(url, timeout, num_retries - 1)
                else:
                    print('开始使用代理')
                    time.sleep(10)
                    IP = ''.join(
                        str(random.choice(self.iplist)).strip())  # 下面有解释哦
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy,)  # 代理不为空的时候

        else:  # 当代理不为空
            try:
                # 将从self.iplist中获取的字符串处理成我们需要的格式（处理了些什么自己看哦，这是基础呢）
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = {'http': IP}  # 构造成一个代理
                # 使用代理获取response
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            except:

                if num_retries > 0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print('正在更换代理，10S后将重新获取倒数第', num_retries, '次')
                    print('当前代理是：', proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print('代理也不好使了！取消代理')
                    return self.get(url, 3)


request = download()
