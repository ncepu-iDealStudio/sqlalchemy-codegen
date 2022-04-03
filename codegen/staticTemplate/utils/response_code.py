#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 User defined Error code.
"""


class RET:
    OK = "2000"

    NODATA = "2001"
    DATAEXIST = "2002"
    DATAERR = "2003"
    PARAMERR = "4000"
    SESSIONERR = "4001"
    LOGINERR = "4002"
    USERERR = "4003"
    ROLEERR = "4004"
    PWDERR = "4005"
    REQERR = "4006"
    IPERR = "4007"
    INTERNALERR = "5000"
    DBERR = "5001"
    THIRDERR = "5002"
    IOERR = "5003"
    UNKOWNERR = "5004"


error_map_CN = {
    RET.OK: u"成功",
    RET.NODATA: u"无数据",
    RET.DATAEXIST: u"数据已存在",
    RET.DATAERR: u"数据错误",
    RET.PARAMERR: u"参数错误",
    RET.SESSIONERR: u"用户未登录",
    RET.LOGINERR: u"用户登录失败",
    RET.USERERR: u"用户不存在或未激活",
    RET.ROLEERR: u"用户身份错误",
    RET.PWDERR: u"密码错误",
    RET.REQERR: u"非法请求或请求次数受限",
    RET.IPERR: u"IP受限",

    RET.DBERR: u"数据库查询错误",
    RET.THIRDERR: u"第三方系统错误",
    RET.IOERR: u"文件读写错误",
    RET.UNKOWNERR: u"未知错误",
}

error_map_EN = {
    RET.OK: "successfully!",
    RET.NODATA: "no data!",
    RET.DATAEXIST: "data exist!",
    RET.DATAERR: "data error!",
    RET.PARAMERR: "parameter error!",
    RET.SESSIONERR: "user not logged in!",
    RET.LOGINERR: "user login failed!",
    RET.USERERR: "user does not exist or not activation! ",
    RET.ROLEERR: "user role error!",
    RET.PWDERR: "password error!",
    RET.REQERR: "illegal request or limited number of requests",
    RET.IPERR: "IP restricted!",

    RET.DBERR: "database query error",
    RET.THIRDERR: "third party system error",
    RET.IOERR: "file read or write error!",
    RET.UNKOWNERR: "unknown error!",
}
