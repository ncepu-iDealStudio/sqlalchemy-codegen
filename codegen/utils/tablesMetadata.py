#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:tablesMetadata.py.py
# author:Nathan
# datetime:2021/8/26 14:56
# software: PyCharm

"""
    Get metadata of all tables
"""
import json
import os.path

from .commons import str_to_all_small, str_to_little_camel_case, str_to_big_camel_case


class TableMetadata(object):
    TYPE_MAPPING = ""

    @classmethod
    def get_tables_metadata(cls, metadata, reflection_views) -> dict:
        """
            获取数据库数据
            :param metadata: sqlalchemy元数据
            :param reflection_views: 需要反射的视图名称列表
        """

        from ..main import workPath
        conf_path = os.path.join(os.path.abspath(workPath), 'config')
        with open(os.path.join(conf_path, 'datatype_map.json'), 'r', encoding='utf-8') as f:
            cls.TYPE_MAPPING = json.load(f)
        # Get all tables object
        table_objs = metadata.tables.values()
        table_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        for table in table_objs:

            table_name = str(table)
            table_dict[table_name] = {}
            table_dict[table_name]['table_name'] = table_name
            table_dict[table_name]['table_name_all_small'] = str_to_all_small(table_name)
            table_dict[table_name]['table_name_little_camel_case'] = str_to_little_camel_case(table_name)
            table_dict[table_name]['table_name_big_camel_case'] = str_to_big_camel_case(table_name)

            # 如果该表是一个视图
            if table_name in reflection_views:
                table_dict[table_name]['is_view'] = True
                table_dict[table_name]['filter_field'] = []

                table_dict[table_name]['columns'] = []
                for column in table.columns.values():
                    temp_column_dict = {
                        "field_name": str(column.name),
                    }

                    for type_ in cls.TYPE_MAPPING:
                        if str(metadata.bind.url).split('+')[0] != type_['database']:
                            continue
                        for python_type, sql_type_list in type_['data_map'].items():
                            if str(column.type).lower() in sql_type_list:
                                temp_column_dict['field_type'] = python_type
                                break

                    temp_column_dict.setdefault('field_type', 'str')
                    table_dict[table_name]['columns'].append(temp_column_dict)

                continue

            table_dict[table_name]['is_view'] = False

            from sqlalchemy.engine import reflection
            insp = reflection.Inspector.from_engine(metadata.bind)
            # 初始化为空列表
            table_dict[table_name]['primary_key_columns'] = insp.get_pk_constraint(table_name)['constrained_columns']
            table_dict[table_name]['columns'] = {}

            # Traverse each columns to get corresponding attributes
            for column in table.columns.values():
                table_dict[table_name]['columns'][str(column.name)] = {}
                table_dict[table_name]['columns'][str(column.name)]['name'] = str(column.name)

                for type_ in cls.TYPE_MAPPING:
                    if str(metadata.bind.url).split('+')[0] != type_['database']:
                        continue
                    for python_type, sql_type_list in type_['data_map'].items():
                        if str(column.type).lower() in sql_type_list:
                            table_dict[table_name]['columns'][str(column.name)]['type'] = python_type
                            break
                table_dict[table_name]['columns'][str(column.name)].setdefault('type', 'str')

                # 是否自动递增
                table_dict[table_name]['columns'][str(column.name)][
                    'is_autoincrement'] = True if column.autoincrement is True else False

                # 是否可以为空
                table_dict[table_name]['columns'][str(column.name)]['nullable'] = column.nullable

                # 是否存在默认值
                table_dict[table_name]['columns'][str(column.name)][
                    'is_exist_default'] = True if column.server_default is not None else False

        return table_dict
