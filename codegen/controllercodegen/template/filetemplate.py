#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:filetemplate.py
# author:Itsuka
# datetime:2021/8/26 10:27
# software: PyCharm

"""
    provide file template here
"""


class FileTemplate(object):

    init_flask_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

    init_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "{databaseUrl}"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

"""

    basic_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-

{imports}


class {class_name}({parent_model}):
"""

    flask_add_template = """
    # add
    @classmethod
    def add(cls, **kwargs):
        try:
            model = {parent_model}(
                {column_init}
            )
            db.session.add(model)
            db.session.commit()
            results = {{
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {add_result_primary_key}
            }}
            return {{'code': "200", 'message': "成功！", 'data': results}}
            
        except Exception as e:
            db.session.rollback()
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    flask_get_template = """
    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            {get_filter_list}
            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            {model_lower}_info = db.session.query(cls).filter(*filter_list)
            
            count = {model_lower}_info.count()
            pages = math.ceil(count / size)
            {model_lower}_info = {model_lower}_info.limit(size).offset((page - 1) * size).all()

            results = cls.to_dict({model_lower}_info)
            return {{'code': "200", 'message': "成功！", 'totalCount': count, 'totalPage': pages, 'data': results}}
            
        except Exception as e:
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    flask_delete_template_physical = """
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = []
            {filter_list_init}
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            
            if not res.first():
                return {{'code': "5001", 'message': "数据库错误", 'error': "数据不存在"}}

            results = {{
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            res.delete()
            db.session.commit()

            return {{'code': "200", 'message': "成功！", 'data': results}}

        except Exception as e:
            db.session.rollback()
            
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    flask_update_template_physical = """
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            filter_list = []
            {filter_list_init}
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            if not res.first():
                return {{'code': "5001", 'message': "数据库错误", 'error': "数据不存在"}}
                
            results = {{
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            
            res.update(kwargs)
            db.session.commit()
            
            return {{'code': "200", 'message': "成功！", 'data': results}}

        except Exception as e:
            db.session.rollback()
            
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    add_template = """
    # add
    @classmethod
    def add(cls, **kwargs):        
        try:
            model = {parent_model}(
                {column_init}
            )
            session.add(model)
            session.commit()
            results = {{
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {add_result_primary_key}
            }}
            return {{'code': "200", 'message': "成功！", 'data': results}}

        except Exception as e:
            session.rollback()
            
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            session.close()
"""

    get_template = """
    # get
    @classmethod
    def get(cls, **kwargs):        
        try:
            filter_list = []
            {get_filter_list}
            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            {model_lower}_info = session.query(cls).filter(*filter_list)

            count = {model_lower}_info.count()
            pages = math.ceil(count / size)
            {model_lower}_info = {model_lower}_info.limit(size).offset((page - 1) * size).all()

            results = cls.to_dict({model_lower}_info)
            return {{'code': "200", 'message': "成功！", 'totalCount': count, 'totalPage': pages, 'data': results}}

        except Exception as e:
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            session.close()
"""

    delete_template_physical = """
    # delete
    @classmethod
    def delete(cls, **kwargs):        
        try:
            filter_list = []
            {filter_list_init}
            res = session.query(cls).filter(*filter_list).with_for_update()

            if not res.first():
                return {{'code': "5001", 'message': "数据库错误", 'error': "数据不存在"}}
                
            results = {{
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            res.delete()
            session.commit()

            return {{'code': "200", 'message': "成功！", 'data': results}}

        except Exception as e:
            session.rollback()
            
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            session.close()
"""

    update_template_physical = """
    # update
    @classmethod
    def update(cls, **kwargs):        
        try:
            filter_list = []
            {filter_list_init}
            res = session.query(cls).filter(*filter_list).with_for_update()

            if not res.first():
                return {{'code': "5001", 'message': "数据库错误", 'error': "数据不存在"}}
                
            results = {{
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}

            res.update(kwargs)
            session.commit()

            return {{'code': "200", 'message': "成功！", 'data': results}}

        except Exception as e:
            session.rollback()
            return {{'code': "5001", 'message': "数据库错误", 'data': {{'error': str(e)}}}}
        finally:
            session.close()
"""