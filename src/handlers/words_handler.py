# coding=utf-8
# __author__ = 'Mio'
import logging

from tornado.web import authenticated
from mongoengine import DoesNotExist

from tools.web.base import BaseRequestHandler
from models.word import Word


class ReciteWordsHandler(BaseRequestHandler):
    def get(self):
        self.render("word.html", error=None, word=None)


class OneWordHandler(BaseRequestHandler):
    @authenticated
    def get(self, word):
        try:
            _word = Word.objects(word=word).get()
        except DoesNotExist:
            self.render("word.html", word=None, error="word '{}' not found, sorry".format(word))
            return

        logging.info(_word)
        if _word:
            self.render("word.html", word=_word.format_response(), error=None)
        else:
            self.render("word.html", word=None, error="word {} not found, sorry".format(word))
        return
