# coding=utf-8
# __author__ = 'Mio'

from mongoengine import (Document, DateTimeField, StringField, ListField, ReferenceField, DictField)

from tools.gmongoengine import field_to_json
from tools.gtz import TimeZone


class Word(Document):
    word = StringField(max_length=32, help_text="单词")
    explanation = ListField(StringField(max_length=256), help_text="解释")
    example = ListField(DictField(default={}), default=[], help_text="例句")
    scope = ListField(StringField(max_length=12), default=[], help_text="范围")
    synonyms = ListField(ReferenceField("Word"), default=[], help_text="近义词")

    create_time = DateTimeField(default=TimeZone.utc_now, help_text="创建时间")
    update_time = DateTimeField(default=None, help_text="创建时间")

    meta = {
        'collection': "word",
        'ordering': [
            "create_time"
        ],
        'indexes': [
            {"fields": ["word"], "unique": True}
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
