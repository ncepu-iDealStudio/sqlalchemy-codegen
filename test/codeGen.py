# coding: utf-8
# @Author : lryself
# @Date : 2022/4/1 17:50
# @Software: PyCharm
from __future__ import unicode_literals, division, print_function, absolute_import

import codecs
import importlib

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from sqlacodegen.codegen import CodeGenerator


def import_dialect_specificities(engine):
    dialect_name = '.' + engine.dialect.name
    try:
        importlib.import_module(dialect_name, 'sqlacodegen.dialects')
    except ImportError:
        pass


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:lpc123LPC@127.0.0.1:3306/flask_layui_frame?charset=utf8mb4")
    import_dialect_specificities(engine)
    metadata = MetaData(engine)
    metadata.reflect(engine)
    generator = CodeGenerator(metadata)
    outfile = "result"
    generator.render(outfile)
