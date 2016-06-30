# coding=utf-8
# __author__ = 'Mio'

from mongoengine import (Document, DateTimeField, StringField, ListField, ReferenceField, DictField)

from tools.gmongoengine import field_to_json
from tools.gtz import TimeZone
from models.user import User

WORD_FINISHED = "FINISHED"
WORD_UNDO = "UNDO"


class Record(Document):
    user = ReferenceField(User, help_text="用户")
    words = ListField(DictField(), default=[], help_text="单词列表")
    status = StringField(max_length=12, help_text="状态")

    create_time = DateTimeField(default=TimeZone.utc_now, help_text="创建时间")
    update_time = DateTimeField(default=None, help_text="创建时间")

    meta = {
        'collection': "record",
        'ordering': [
            "create_time"
        ],
        'indexes': [
            "create_time"
        ]
    }

    def format_response(self, expect_fields=None, skip_fields=None):
        json_data = {}
        if expect_fields is None:
            expect_fields = set([])
        if skip_fields is None:
            skip_fields = set([])

        if not expect_fields:
            anti_skip_fields = set([f for f in self]) - skip_fields
            expect_fields = anti_skip_fields

        for field in expect_fields:
            value = self[field]
            json_data[field] = field_to_json(value)
        return json_data
