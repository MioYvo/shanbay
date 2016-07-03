# coding=utf-8
# __author__ = 'Mio'

from mongoengine import (Document, DateTimeField, StringField, ListField, ReferenceField, DictField)

from tools.gmongoengine import field_to_json
from tools.gtz import TimeZone
from models.user import User

WORD_FINISHED = "WORD_FINISHED"
WORD_UNDONE = "WORD_UNDONE"

RECORD_FINISHED = "RECORD_FINISHED"
RECORD_UNDONE = "RECORD_UNDONE"


class Record(Document):
    user = ReferenceField(User, help_text="用户")
    words = ListField(DictField(), default=[], help_text="单词列表")
    status = StringField(default=RECORD_UNDONE, max_length=24, help_text="状态")

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
            if field == "words":
                value = value[::-1]
            json_data[field] = field_to_json(value)
        return json_data

    @property
    def next_word(self):
        next_word = "END"
        for word in self.words:
            if word['status'] == WORD_UNDONE:
                next_word = word['word']
        return next_word
