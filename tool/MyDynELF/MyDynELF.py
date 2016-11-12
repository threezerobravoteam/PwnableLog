#!/usr/bin/env python
# coding=utf-8
# author:muhe
# based on http://uaf.io/exploitation/misc/2016/04/02/Finding-Functions.html

class MyDynELF(object):
	"""docstring for MyDynELF"""
	def __init__(self, arg):
		super(MyDynELF, self).__init__()
		self.arg = arg
		