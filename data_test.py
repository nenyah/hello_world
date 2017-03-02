#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
词频统计
Version:    2016-08-24
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import string

path = r'E:\Work\wwwroot\Code\Walden.txt'

with open(path,'r', encoding='utf-8') as text:
	words = [raw_word.strip(string.punctuation).lower() for raw_word in text.read().split()]
	words_index = set(words)
	counts_dict = {index:words.count(index) for index in words_index}

for word in sorted(counts_dict,key=lambda x: counts_dict[x],reverse=True):
	print('{} -- {} times'.format(word,counts_dict[word]))