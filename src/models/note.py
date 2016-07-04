# coding=utf-8
# __author__ = 'Mio'

from mongoengine import (Document, DateTimeField, StringField, ListField, ReferenceField, DictField, DoesNotExist)

from tools.gmongoengine import field_to_json
from tools.gtz import TimeZone


class Note(Document):
    word = StringField(max_length=32, help_text="单词")
    notes = ListField(DictField(), default=[], help_text="范围")

    create_time = DateTimeField(default=TimeZone.utc_now, help_text="创建时间")
    update_time = DateTimeField(default=None, help_text="创建时间")

    meta = {
        'collection': "note",
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

    def add_notes(self, note, user):
        """
        只保留5条
        :param note:
        :param user:
        :return:
        """
        self.notes.append({"user": user.format_response(), "content": note, "create_time": TimeZone.utc_now()})
        self.notes = self.notes[-5:][::-1]
        self.save()

    @classmethod
    def get_note(cls, word):
        try:
            note_record = cls.objects(word=word).get()
        except DoesNotExist:
            note_record = Note(word=word).save()
        return note_record
