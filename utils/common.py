#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen
# author:PigKnight
# datetime:2021/8/21 11:28
# software: PyCharm

"""
    General method
"""


# 连字符转驼峰
def str_format_convert(string):
    new_string = ''
    for word in string.split('_'):
        if new_string:
            new_string += word.lower().capitalize()
        else:
            new_string = word
    return new_string


# 字符串转全小写
def str_to_all_small(string):
    new_string = string.replace('_', '').lower()

    return new_string


# 字符串转小驼峰
def str_to_little_camel_case(string):
    new_string = ''
    for word in string.split('_'):
        if new_string:
            new_string += word[0].upper() + word[1:]
        else:
            new_string = word

    return new_string


# 字符串转大驼峰
def str_to_big_camel_case(string):
    new_string = ''
    for word in string.split('_'):
        new_string += word[0].upper() + word[1:]

    return new_string


if __name__ == '__main__':
    ll = ['user_info', 'userInfo', 'userinfo']
    for l in ll:
        print(l, '->', str_to_little_camel_case(l))
