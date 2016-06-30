# coding=utf-8
# __author__ = 'Mio'
import logging

from bson import ObjectId
from schema import Schema, Optional, Or
from tornado.web import authenticated, Finish
from mongoengine import DoesNotExist

from tools.web.base import BaseRequestHandler
from models.word import Word
from models.record import Record, WORD_FINISHED, WORD_UNDO
from tools.web.escape import schema_utf8


class ReciteWordsHandler(BaseRequestHandler):
    @authenticated
    def get(self):
        """
        生成背诵列表
        :return:
        """
        user = self.get_current_user_mongo()

        # 获取上次未完成的背诵

        # 已背的单词们
        # Pipeline
        pipeline = [
            # Stage 1
            {
                "$match": {
                    "user": user.pk,
                }
            },

            # Stage
            {
                "$unwind": "$words"
            },

            # Stage
            {
                "$match": {
                    "words.status": WORD_FINISHED
                }
            },

            # Stage
            {
                "$group": {
                    "_id": "$user",
                    "words_recited": {"$addToSet": "$words.word"}
                }
            },

            # Stage
            {
                "$project": {
                    "_id": 0,
                    "words_recited": 1
                }

            }
        ]
        logging.info(user.pk)
        recited_words = Record.objects(user=user, words__status=WORD_FINISHED).aggregate(*pipeline)
        for rst in recited_words:
            wait_words = Word.objects(word__nin=rst['words_recited'], scope__in=[user.scope]).limit(user.quota)
            self.write_response([word['word'] for word in wait_words])
            return
        self.write_response([])


class OneWordReciteHandler(BaseRequestHandler):
    @authenticated
    def post(self, word):
        """
        完成一个单词
        :param word:
        :return:
        """
        user = self.get_current_user_mongo()
        data = self.post_schema()
        try:
            Record.objects(
                pk=ObjectId(data['record_id']),
                user=user,
                words__word=word
            ).update_one(**{'set__words__$__status': WORD_FINISHED})
        except DoesNotExist as e:
            logging.exception(e)
            self.write_error_response(e.message)
            raise Finish
        else:
            # TODO 下一页 word
            self.render("")
            return

    def post_schema(self):
        try:
            data = Schema({
                "record_id": schema_utf8,
                Optional("to_status", default=WORD_FINISHED): Or(WORD_FINISHED, WORD_UNDO)
            }).validate(self.get_body_args())
        except Exception as e:
            logging.error(e)
            self.write_parse_args_failed_response(content=e.message)
            raise Finish
        else:
            return data


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
