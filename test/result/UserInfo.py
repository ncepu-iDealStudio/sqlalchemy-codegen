# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, MetaData, SmallInteger, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class UserInfo(Base):
    __tablename__ = 'user_info'

    user_id = Column(Integer, primary_key=True, info='自增主键, UserMixin.get_id()')
    user_number = Column(Integer, nullable=False, unique=True, info='工号, 重要')
    user_name = Column(String(20, 'utf8mb4_general_ci'), nullable=False, info='用户名')
    realname = Column(String(20, 'utf8mb4_general_ci'), nullable=False, info='姓名')
    email = Column(String(100, 'utf8mb4_general_ci'), server_default=FetchedValue(), info='邮箱')
    role_id = Column(Integer, index=True, server_default=FetchedValue(), info='角色标识ID')
    is_deleted = Column(SmallInteger, index=True, server_default=FetchedValue(), info='数据有效性：\\r\\n1-有效\\r\\n2-无效')
