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

    init_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

    basic_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-
{imports}


class {class_name}({parent_model}):
"""

    add_template = """
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
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
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
            
            {model_lower}_info = db.session.query(cls).filter(*filter_list)
            
            count = {model_lower}_info.count()
            pages = math.ceil(count / size)
            {model_lower}_info = {model_lower}_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict({model_lower}_info)
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}}
            
        except Exception as e:
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

#     delete_template_physical = """
#     # delete
#     @classmethod
#     def delete(cls, **kwargs):
#         try:
#             filter_list = []
#             if kwargs.get('{primary_key}'):
#                 primary_key_list = []
#                 for primary_key in str(kwargs.get('{primary_key}')).replace(' ', '').split(','):
#                     primary_key_list.append(cls.{primary_key} == primary_key)
#                 filter_list.append(or_(*primary_key_list))
#
#             else:
#                 {delete_filter_list}
#             res = db.session.query(cls).filter(*filter_list).with_for_update()
#
#             results = {{
#                 '{primary_key}': [],
#                 'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             }}
#             for query_model in res.all():
#                 results['{primary_key}'].append(query_model.{primary_key})
#
#             res = res.delete()
#             db.session.commit()
#
#             return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}
#
#         except Exception as e:
#             db.session.rollback()
#             loggings.exception(1, e)
#             return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
#         finally:
#             db.session.close()
# """
#
#     delete_template_logic = """
#     # delete
#     @classmethod
#     def delete(cls, **kwargs):
#         try:
#             filter_list = [cls.{logical_delete_mark} == 0]
#             if kwargs.get('{primary_key}'):
#                 primary_key_list = []
#                 for primary_key in str(kwargs.get('{primary_key}')).replace(' ', '').split(','):
#                     primary_key_list.append(cls.{primary_key} == primary_key)
#                 filter_list.append(or_(*primary_key_list))
#
#             else:
#                 {delete_filter_list}
#             res = db.session.query(cls).filter(*filter_list).with_for_update()
#
#             results = {{
#                 '{primary_key}': [],
#                 'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             }}
#             for query_model in res.all():
#                 results['{primary_key}'].append(query_model.{primary_key})
#
#             res = res.update({{'{logical_delete_mark}': 1}})
#             db.session.commit()
#
#             return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}
#
#         except Exception as e:
#             db.session.rollback()
#             loggings.exception(1, e)
#             return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
#         finally:
#             db.session.close()
# """

    delete_template_physical = """
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = []
            {filter_list_init}
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {{
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            res.delete()
            db.session.commit()

            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    delete_template_logic = """
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = [cls.{logical_delete_mark} == 0]
            {filter_list_init}
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {{
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            {single_primary_key_result_append}
            res.update({{'{logical_delete_mark}': 1}})
            db.session.commit()

            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
    """

    update_template_physical = """
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            filter_list = []
            {filter_list_init}
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {{
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            
            res.update(kwargs)
            db.session.commit()
            
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    update_template_logic = """
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            filter_list = [cls.{logical_delete_mark} == 0]
            {filter_list_init}
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {{
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                {results_primary_keys}
            }}
            
            res.update(kwargs)
            db.session.commit()

            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""

    add_list_template = """
    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = json.loads(kwargs.get('{parent_model}List'))
        model_list = []
        for param_dict in param_list:
            {add_list_business_key_init}
            model = {parent_model}(
                {add_list_column_init}
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {{
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }}
            for model in model_list:
                added_record = {{}}
                {added_record_primary_keys}
                results['added_records'].append(added_record)
            
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
        finally:
            db.session.close()
"""
