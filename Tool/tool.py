#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
tools set
Version:    2016-09-22
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import os

def get_filenames(path):
	"""return full filename from a path"""
	filenames = []
	for i in os.walk(path):
		for filename in i[-1]:
			full_filename = os.path.join(i[0],filename)
			filenames.append(full_filename)
	return filenames