# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, MetaData, SmallInteger, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class SysLogUser(Base):
    __tablename__ = 'sys_log_user'

    log_id = Column(BigInteger, primary_key=True, info='自增主键')
    log_time = Column(DateTime, index=True, server_default=FetchedValue(), info='日志写入时间')
    log_action = Column(String(50, 'utf8mb4_general_ci'), nullable=False, index=True, info='操作动作')
    log_operator = Column(String(20, 'utf8mb4_general_ci'), nullable=False, index=True, info='操作者姓名')
    log_content = Column(String(5000, 'utf8mb4_general_ci'), server_default=FetchedValue(), info='操作详情')
    log_status = Column(SmallInteger, nullable=False, index=True, server_default=FetchedValue(), info='操作是否成功')
