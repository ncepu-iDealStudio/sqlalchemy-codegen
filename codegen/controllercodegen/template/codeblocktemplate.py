#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codeblocktemplate.py
# author:Itsuka
# datetime:2021/8/26 10:32
# software: PyCharm

"""
    provide code block template here
"""


class CodeBlockTemplate(object):

    imports = """
import datetime
import math

from models import db
from models.{model_name} import {parent_model}
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings"""

    add_column_init = """{column}=kwargs.get('{column}'),
                """

    rsa_add = """{column}=RSAEncryptionDecryption.encrypt(kwargs.get('{column}')) if kwargs.get('{column}') else None,
                """

    business_key_add = """{column}={column},
                """

    get_filter_num = """if kwargs.get('{column}') is not None:
                    filter_list.append(cls.{column} == kwargs.get('{column}'))
                """

    get_filter_str = """if kwargs.get('{column}'):
                    filter_list.append(cls.{column} == kwargs.get('{column}'))
                """

    get_filer_list_logic = 'cls.{logical_delete_mark} == 0'

    rsa_get_filter_num = """if kwargs.get('{column}') is not None:
                    filter_list.append(cls.{column} == RSAEncryptionDecryption.encrypt(kwargs.get('{column}')))
                """

    rsa_get_filter_str = """if kwargs.get('{column}'):
                    filter_list.append(cls.{column} == RSAEncryptionDecryption.encrypt(kwargs.get('{column}')))
                """

    rsa_update = """if kwargs.get('{column}'):
                kwargs['{column}'] = RSAEncryptionDecryption.encrypt(kwargs['{column}'])
            """

    business_key_init = """from utils.generate_id import GenerateID
        {business_key} = GenerateID.{rule}()
        """

    add_list_column_init = """{column}=param_dict.get('{column}'),
                """

    add_list_business_key_init = """from utils.generate_id import GenerateID
            {business_key} = GenerateID.{rule}()
            """

    add_list_rsa_add = """{column}=RSAEncryptionDecryption.encrypt(param_dict.get('{column}')),
                """

    single_primary_key_get_filter = """if kwargs.get('{primary_key}'):
                filter_list.append(cls.{primary_key} == kwargs['{primary_key}'])
            else:
                {get_filter_list}
"""

    delete_filter = """if kwargs.get('{primary_key}'):
                primary_key_list = []
                for primary_key in str(kwargs.get('{primary_key}')).replace(' ', '').split(','):
                    primary_key_list.append(cls.{primary_key} == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                {delete_filter_list}"""

    multi_primary_key_filter = """filter_list.append(cls.{primary_key} == kwargs.get('{primary_key}'))
            """

    results_primary_keys = """'{primary_key}': []"""

    multi_primary_key_result = """'{primary_key}': res.first().{primary_key},
                """

    add_result_primary_key = """'{primary_key}': model.{primary_key},
                """

    # add_list_result_primary_key = """'{primary_key}': [],"""
    #
    # multi_primary_key_add_list_result = """'records': []"""

    multi_primary_key_add_list_result_detail_keys = """added_record['{primary_key}'] = model.{primary_key}
                """

    single_primary_key_result_append = """for query_model in res.all():
                results['{primary_key}'].append(query_model.{primary_key})
"""

    multi_get_filter_num = """if kwargs.get('{column}') is not None:
                filter_list.append(cls.{column} == kwargs.get('{column}'))
            """

    multi_get_filter_str = """if kwargs.get('{column}'):
                filter_list.append(cls.{column} == kwargs.get('{column}'))
            """

    multi_rsa_get_filter_num = """if kwargs.get('{column}') is not None:
                filter_list.append(cls.{column} == RSAEncryptionDecryption.encrypt(kwargs.get('{column}')))
            """

    multi_rsa_get_filter_str = """if kwargs.get('{column}'):
                filter_list.append(cls.{column} == RSAEncryptionDecryption.encrypt(kwargs.get('{column}')))
            """
