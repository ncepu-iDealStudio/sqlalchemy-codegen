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
import os
import sys


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


def cur_file_dir():
    '''
    用于找到当前文件的目录

    :return:返回一个绝对路径
    '''
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


if __name__ == '__main__':
    ll = ['user_info', 'userInfo', 'userinfo']
    for l in ll:
        print(l, '->', str_to_little_camel_case(l))
