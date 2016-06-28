#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-11-09 19:56:43
# @Author  : Jim Zhang (jim.zoumo@gmail.com)
# @Github  : https://github.com/zoumo

from bson import ObjectId
from datetime import datetime
from tools.gtz import TimeZone
from mongoengine import EmbeddedDocument, Document


def field_to_json(value):

    ret = value
    if isinstance(value, ObjectId):
        ret = str(value)
    elif isinstance(value, datetime):
        ret = TimeZone.datetime_to_str(value)
    elif isinstance(value, EmbeddedDocument):
        if hasattr(value, "format_response"):
            ret = value.format_response()
    elif isinstance(value, Document):
        if hasattr(value, "format_response"):
            ret = value.format_response()
        else:
            ret = str(value.id)
    elif isinstance(value, list):
        ret = [field_to_json(_) for _ in value]
    elif isinstance(value, dict):
        ret = {k: field_to_json(v) for k, v in value.iteritems()}
    return ret
