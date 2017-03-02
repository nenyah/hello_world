#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
查看邮箱MX记录
Version:    2016-06-21
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import dns.resolver
import sys

def check(email):
    user_name,domain = email.split('@')
    MX = dns.resolver.query(domain,'MX')
    result = ''
    if MX:
        for info in MX:
            result += 'MX preference = {} Mail exchanger = {}\n'.format(info.preference,
info.exchange)
    else:
        result = "{} dosn't exist".format(email)
    return result

if __name__ == '__main__':
    emails = sys.argv[1:]
    print(*map(check,emails))
    

