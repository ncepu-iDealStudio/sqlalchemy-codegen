#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkTable.py
# author:Itsuka
# datetime:2021/8/25 9:53
# software: PyCharm

"""
    检验表是否符合生成规则
"""

import keyword

from .loggings import loggings
from .tablesMetadata import TableMetadata


class CheckTable(object):

    # check the Primary key
    # 检查table主键
    @classmethod
    def check_primary_key(cls, table_dict):
        """
        根据代码生成模式，自动读取所有表或所需表，检验主键后返回合规的表列表
        :return: 符合规范的表名列表，即有且仅有一个主键，没有符合规范的情况下返回None
        """

        available_tables = []
        invalid_tables = []

        for table in table_dict.values():
            if table['is_view']:
                # 是一个视图，不进行检查
                continue
            elif len(table['primary_key_columns']) == 0:
                # 表中没有主键
                invalid_tables.append(table['table_name'])
                loggings.warning(1, 'table {0} do not have a primary key'.format(table['table_name']))
            # elif len(table['primary_key_columns']) > 1:
            #     # 表中有复数个主键
            #     invalid_tables.append(table['table_name'])
            #     loggings.warning(1, 'table {0} has multiple primary keys'.format(table['table_name']))
            else:
                available_tables.append(table['table_name'])

        return available_tables, invalid_tables

    # check keywords of python in tables
    # 检查表名和字段名，是否和Python的关键字冲突
    @classmethod
    def check_keyword_conflict(cls, table_dict):
        """
        check whether the table name or column name is a keyword of python
        :return: True while no table name is a keyword, else return False
        """

        available_table = []
        invalid_table = []

        for table in table_dict.values():

            if table['is_view']:
                # 是一个视图，不进行检查
                continue

            flag = True

            # 检查表名是否为python关键字
            if keyword.iskeyword(table['table_name']):
                loggings.warning(1, 'table "{0}" is a keyword of python'.format(table['table_name']))
                flag = False

            for column in table['columns'].values():
                # 检查表字段是否为python关键字
                if keyword.iskeyword(column['name']):
                    loggings.warning(1, 'column "{0}.{1}" is a keyword of python'.format(table['table_name'],
                                                                                         column['name']))
                    flag = False

            if flag:
                available_table.append(table['table_name'])
            else:
                invalid_table.append(table['table_name'])

        return available_table, invalid_table

    # 入口函数定义
    @classmethod
    def main(cls, metadata, reflection_views):
        """
            建立数据库连接时对表进行检查，筛去没有唯一自增主键、表名/字段名与Python关键字有冲突的表
            :param metadata: 数据库元数据
            :param reflection_views: 需要反射的视图名称列表
        """

        table_dict = TableMetadata.get_tables_metadata(metadata, reflection_views)
        invalid_tables = {}

        # check table primary key
        available_table, invalid_table = cls.check_primary_key(table_dict)
        invalid_tables['primary_key'] = invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        # check the keyword
        available_table, invalid_table = cls.check_keyword_conflict(table_dict)
        available_tables = available_table
        invalid_tables['keyword'] = invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        if len(invalid_tables) > 0:
            loggings.warning(
                1,
                "A total of {0} tables check passed."
                "The following {1} tables do not meet the specifications and cannot be generated: {2}."
                    .format(
                        len(available_tables),
                        len(invalid_tables['primary_key'] + invalid_tables['keyword']),
                        ",".join(invalid_tables['primary_key'] + invalid_tables['keyword'])
                    )
            )

            return table_dict, invalid_tables

        loggings.info(1, "All table checks passed, a total of {0} tables.".format(len(available_tables)))

        return table_dict, invalid_tables
