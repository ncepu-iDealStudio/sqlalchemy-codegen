#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:seting.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

"""
  应用的配置加载项
"""

import os
from configparser import ConfigParser
from urllib import parse

os.chdir(os.path.dirname(os.path.dirname(__file__)))


class Settings(object):

    def __init__(self, session_id):

        # 配置文件目录
        CONFIG_DIR = "config/config_" + str(session_id) + ".conf"
        CONFIG = ConfigParser()

        # 读取配置文件
        CONFIG.read(CONFIG_DIR, encoding='utf-8')

        # 生成项目的名称
        self.PROJECT_NAME = CONFIG['PARAMETER']['PROJECT_NAME']
        # 项目生成的目标路径
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 目标目录
        self.TARGET_DIR = os.path.join(self.BASE_DIR, CONFIG['PARAMETER']['TARGET_DIR']) + "/" + CONFIG['PARAMETER'][
            'TARGET_DIR'] + "_" + str(session_id)
        # 项目目录
        self.PROJECT_DIR = os.path.join(self.TARGET_DIR, self.PROJECT_NAME)
        # 生成项目API的版本
        self.API_VERSION = CONFIG['PARAMETER']['API_VERSION'].replace('.', '_')
        # 定义静态资源文件路径
        self.STATIC_RESOURCE_DIR = os.path.join(self.BASE_DIR, 'static')

        # 数据库dialect到driver的映射
        driver_dict = {
            'mysql': 'pymysql',
            'mssql': 'pymssql',
            'oracle': 'cx_oracle',
            'postgresql': 'psycopg2'
        }

        # 读取数据库配置
        self.DIALECT = CONFIG['DATABASE']['DIALECT']
        self.DRIVER = driver_dict[self.DIALECT]
        self.USERNAME = CONFIG['DATABASE']['USERNAME']
        self.PASSWORD = CONFIG['DATABASE']['PASSWORD']
        self.HOST = CONFIG['DATABASE']['HOST']
        self.PORT = CONFIG['DATABASE']['PORT']
        self.DATABASE = CONFIG['DATABASE']['DATABASE']

        # model层配置
        self.MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            self.DIALECT,
            self.DRIVER,
            self.USERNAME,
            parse.quote_plus(self.PASSWORD),
            self.HOST,
            self.PORT,
            self.DATABASE
        )
