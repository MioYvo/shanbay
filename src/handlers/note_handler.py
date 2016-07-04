# coding=utf-8
# __author__ = 'Mio'
import logging

from schema import Schema
from tornado.web import Finish
from tools.web.base import BaseRequestHandler
from tools.web.escape import schema_utf8

from models.note import Note


class OneWordNoteHandler(BaseRequestHandler):
    def post(self, word):
        note = self.post_schema()['note']

        user = self.get_current_user_mongo()

        note_record = Note.get_note(word)

        note_record.add_notes(note, user)
        self.write_response(note_record.format_response())
        return

    def post_schema(self):
        try:
            data = Schema({
                "note": schema_utf8
            }).validate(self.get_body_args())
        except Exception as e:
            logging.error(e)
            self.write_parse_args_failed_response(content=e.message)
            raise Finish
        else:
            return data
