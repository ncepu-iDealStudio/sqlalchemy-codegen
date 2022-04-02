#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 some common tools or fuctions your api project maybe need!
"""

from werkzeug.routing import BaseConverter
from datetime import datetime as cdatetime
from datetime import date, time
from flask_sqlalchemy import Model
from sqlalchemy import DateTime, Numeric, Date, Time
import json


# 定义正则转换器
class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类初始化方法
        super(ReConverter, self).__init__(url_map)

        # 保存正则表达式
        self.regex = regex


def put_remove_none(**args):
    """
    PUT方法更新时，如果参数不是必填，用reqparse检验参数会将数据转为空，
    数据库有的字段可能不允许为空，故用该方法解决
    :param args: 原始数据字典
    :return: 除去None数据的字典
    """
    for key in list(args.keys()):
        if args[key] is None or args[key] == '':
            del args[key]
            continue

    args = dict(args)
    return args


# flask-sqlachemy查询结果（对象）转换为字典,下面的所有方法为一个模块，使用时直接调用该方法即可
def query_to_dict(models):
    if models is None:
        return []
    if isinstance(models, list):
        if not models:
            return []
        if isinstance(models[0], Model):
            lst = []
            for model in models:
                gen = model_to_dict(model)
                dit = dict((g[0], g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            res = result_to_dict(models)
            return res
    else:
        if isinstance(models, Model):
            gen = model_to_dict(models)
            dit = dict((s[0], s[1]) for s in gen)
            return dit
        else:
            res = dict(zip(models.keys(), models))
            find_datetime(res)
            return res


# 当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(zip(r.keys(), r)) for r in results]
    # 这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res


def model_to_dict(model):  # 这段来自于参考资源
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        yield (col.name, value)


def find_datetime(value):
    for v in value:
        if isinstance(value[v], cdatetime):
            value[v] = convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改


def convert_datetime(value):
    """
    数据库datetime类型转时间字符串
    :param value:
    :return:
    """
    if value:
        if isinstance(value, (cdatetime, DateTime)):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, (date, Date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (Time, time)):
            return value.strftime("%H:%M:%S")
    else:
        return ""


def is_json(json_str):
    """
    验证json字符串是否合法
    :param json_str:
    :return:
    """
    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True


def list_to_tree(id, parent_id, data):
    """
    将列表结构数据转换为列表树状结构
    :param id: 主键id  字符串
    :param parentid: 父id 字符串
    :param data:要转换的列表结构数据
    :return:转换后的列表树状结构数据
    """
    res = {}
    for index, value in enumerate(data):
        data[index][id] = int(data[index][id])
        data[index][parent_id] = int(data[index][parent_id])
    for v in data:
        # 以id为key，存储当前元素数据
        res.setdefault(v[id], v)
    for v in data:
        res.setdefault(v[parent_id], {}).setdefault('Children', []).append(v)
        # 这里默认的关联关系，v的内存地址是一致的，所以后续修改只后，关联的结构也会变化。
    return res[0]['Children']


def tree(data, root, root_field, node_field):
    """
    解析list数据为树结构
    :param data:  被解析的数据
    :param root: 根节点值
    :param root_field: 根节点字段
    :param node_field: 节点字段
    :return: list
    """
    for index, value in enumerate(data):
        data[index][node_field] = int(data[index][node_field])
        data[index][root_field] = int(data[index][root_field])

    l = []
    for i in data:
        if i.get(root_field) == root:
            l.append(i)
    for i in data:
        node = i.get(node_field)
        children = []
        for j in data:
            parent = j.get(root_field)
            if node == parent:
                children.append(j)
        i['Children'] = children
    return l
