# coding=utf-8
# __author__ = 'Mio'

from mongoengine import Document, DateTimeField, StringField, IntField

from tools.gmongoengine import field_to_json
from tools.gtz import TimeZone


class User(Document):
    name = StringField(max_length=24, help_text="用户名")
    scope = StringField(max_length=12, help_text="背诵范围")
    quota = IntField(max_value=500, help_text="每日单词配额")
    create_time = DateTimeField(default=TimeZone.utc_now, help_text="创建时间")
    update_time = DateTimeField(default=None, help_text="创建时间")

    meta = {
        'collection': 'user',
        'ordering': [
            'create_time',
        ],
        'indexes': [
            "name",
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
