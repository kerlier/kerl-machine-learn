#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
正则表达式： 就是从左到右匹配一个字符串

^表示开头
$表示结尾
'''
import re

res = re.match(r'^.*$', 'aaaaa')
# match返回
print(res.group())

# [] 表示字符的取值范围
res = re.findall(r'([Cc]at)', 'The cat Cat cat cat sat on the mat')
print(res)

# 寻找ar结尾的3个字符串
res = re.findall('(.ar)', 'The car parked in the garage.')
print(res)

# [^c] ^ 如果是第一个，表示开头。但是在其他,表示的否定
res = re.findall(r'[^cg]ar', 'The car parked in the garage.')
print(res)

res = re.findall(r'[a-z]*', 'The car parked in the garage')
print(res)