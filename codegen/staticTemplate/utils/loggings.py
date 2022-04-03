#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    操作日志记录类定义
"""

import sys
from loguru import logger


class Loggings(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def info(self, location, msg):
        Loggings.log_filter(location)

        return logger.info(msg)

    def debug(self, location, msg):
        Loggings.log_filter(location)
        return logger.debug(msg)

    def warning(self, location, msg):
        Loggings.log_filter(location)
        return logger.warning(msg)

    def error(self, location, msg):
        Loggings.log_filter(location)
        return logger.error(msg)

    def exception(self, location, msg):
        Loggings.log_filter(location)
        return logger.exception(msg)

    @staticmethod
    def log_filter(location):
        # 日志和控制台都出现
        if location == 1:
            logger.remove()
            logger.add(sys.stdout)
            logger.add("logs/codegen_log.log", encoding="utf-8", enqueue=True, rotation="100 KB")

        # 只在日志中出现
        elif location == 2:
            logger.remove()
            logger.add("logs/codegen_log.log", encoding="utf-8", enqueue=True, rotation="100 KB")


loggings = Loggings()
