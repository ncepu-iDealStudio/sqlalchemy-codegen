#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkSqlLink.py
# author:Itsuka
# datetime:2021/9/16 12:20
# software: PyCharm

"""
    检验数据库连接是否成功并返回所有表、字段信息（前端用）
"""

from sqlalchemy import create_engine, MetaData, inspect

from codegen.utils.checkTable import CheckTable
from urllib import parse


def check_sql_link(dialect, username, password, host, port, database) -> dict:
    """
    返回所有表、字段信息（前端用）
    :param dialect: 数据库种类
    :param username: 用户名
    :param password: 密码
    :param host: 数据库IP
    :param port: 数据库端口号
    :param database: 要连接的数据库
    :return code: 布尔型，True表示连接成功，False表示连接失败
    :return message: 返回信息
    :return error: 错误信息
    :return data: 所有表的信息及字段
    :return invalid: 检查不通过的表，以列表返还表名
    """
    try:
        driver_dict = {
            'mysql': 'pymysql',
            'mssql': 'pymssql',
            'oracle': 'cx_oracle',
            'postgresql': 'psycopg2'
        }
        password = parse.quote_plus(password)
        url = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(dialect, driver_dict[dialect], username, password, host,
                                                           port, database)
        engine = create_engine(url)
        metadata = MetaData(engine)
        inspector = inspect(engine)
        metadata.reflect(engine, views=True)

    except Exception as e:
        return {'code': False, 'message': str(e), 'error': str(e)}

    table_dict, invalid_tables = CheckTable.main(metadata, inspector.get_view_names())

    data = {
        'table': [],
        'view': []
    }
    for table in table_dict.values():
        if table['is_view']:
            # 是一个视图
            filter_field = []
            for column in table['columns']:
                column['ischecked'] = False
                filter_field.append(column)
            data['view'].append({
                'view': table['table_name'],
                'filter_field': filter_field,
                'ischecked': False
            })
        else:
            # 是一个基本表
            filed = []
            business_key_type = ''
            for column in table['columns'].values():
                if table.get('business_key_column') and column['name'] == table['primary_key_columns'][0]:
                    # 唯一主键不是递增时，需要记录该主键的数据类型
                    business_key_type = column['type']
                if column['name'] in table['primary_key_columns']:
                    # 剔除出主键
                    continue
                else:
                    filed.append({
                        'field_name': column['name'],
                        'field_type': column['type'],
                        'field_encrypt': False
                    })
            data['table'].append({
                'table': str(table['table_name']),
                'businesskeyname': table['business_key_column'].get('column') if table['business_key_column'].get('column') else '',
                'businesskeyrule': '',
                'logicaldeletemark': '',
                'field': filed,
                'businesskeyuneditable': True if table['business_key_column'].get('column') or len(table['primary_key_columns']) > 1 else False,
                "businesskeytype": business_key_type,
                'issave': False
            })
    return {'code': True, 'message': '成功', 'data': data, 'invalid': invalid_tables}


def connection_check(dialect, username, password, host, port, database) -> dict:
    """
    检验数据库连接是否成功
    :param dialect: 数据库种类
    :param username: 用户名
    :param password: 密码
    :param host: 数据库IP
    :param port: 数据库端口号
    :param database: 要连接的数据库
    :return code: 布尔型，True表示连接成功，False表示连接失败
    :return message: 返回信息
    :return error: 错误信息
    """
    try:
        driver_dict = {
            'mysql': 'pymysql',
            'mssql': 'pymssql',
            'oracle': 'cx_oracle',
            'postgresql': 'psycopg2'
        }
        url = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(dialect, driver_dict[dialect], username, password, host,
                                                           port, database)
        engine = create_engine(url)
        metadata = MetaData(engine)
        metadata.reflect(engine)
        return {'code': True, 'message': '数据库连接成功', 'data': ''}
    except Exception as e:
        return {'code': False, 'message': '数据库连接失败', 'error': str(e)}
