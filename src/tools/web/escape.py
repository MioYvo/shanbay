# coding=utf-8
# __author__ = 'Mio'

import re
from schema import And, Use, Or
from tornado.escape import utf8


def power_split(value, separator=',', schema=str):
    assert callable(schema)
    value = utf8(value)
    value = value.strip()
    l = re.split("\s*" + separator + "\s*", value)  # 这个slip直接去除逗号左右的空格
    return [v for v in l if v != '']


schema_utf8 = And(Or(Use(utf8), Use(str)), len)  # 非空
schema_utf8_none = Or(Use(utf8), Use(str))
schema_int = Use(int)
schema_float = Use(float)

# MongoDB object_id
schema_object_id = And(schema_utf8, lambda x: len(x) == 24)
