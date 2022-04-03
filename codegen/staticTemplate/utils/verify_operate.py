#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:verify_operate
# author:Nathan
# datetime:2020/10/12 13:15
# software: PyCharm

"""
   越权访问验证函数
"""

from functools import wraps

from flask import g, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .response_code import RET, error_map_EN


# 定义一个装饰器；用户身份验证（解决垂直越权问题：验证用户的类型是否有权操作调用接口）
def person_info_verify(UserID, UserType, Token, **kwargs):
    """获取装饰器参数
    :param UserID: 接口调用者ID（即登录时存储的UserID）
    :param UserType: 接口调用者用户类型（即登录时存储的UserType）
    :param Token: 用户访问口令
    :param kwargs: 需要验证的用户信息（里面需要包含UserID和UserType）
    """

    def _person_info_verify(func):
        """获得函数"""

        @wraps(func)
        def wrapper(*args, **func_kwargs):
            # 验证合法性
            s = Serializer(current_app.config["SECRET_KEY"])
            try:
                # 解析token 获取Token中的UserID和UserType
                data = s.loads(Token)
                # 如果 接口调用者的UserID和UserType和Token中解析出来的不一致，意味着用户身份不正确
                if UserID != data.get('UserID') or UserType != data.get('UserType'):
                    return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "用户身份错误"})

            except Exception as e:
                return jsonify(code=RET.SESSIONERR, message=error_map_EN[RET.SESSIONERR], data={"error": str(e)})

            # 判断调用者的ID和需要操作的ID是否一致
            if UserID != kwargs.get('UserID') or UserType != kwargs.get('UserType'):
                return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "访问权限不足"})

            return func(*args, **func_kwargs)

        return wrapper

    return _person_info_verify


# 定义一个装饰器: 用户身份验证（解决垂直越权问题：验证用户的类型是否有权操作调用接口）
def verify_usertype(allow_users, *args, **kwargs):
    """
    :param allow_users: List[int] or Set[int] or Tuple[int] 允许访问的权限
    获取装饰器的传参
    """

    def _verify_usertype(func):
        """
        获取函数
        """

        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            """
            获取函数传参
            """
            if g.user.get("UserType") not in allow_users:
                return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "权限不足"})
            return func(*func_args, **func_kwargs)

        return wrapper

    return _verify_usertype
