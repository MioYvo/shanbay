# coding=utf-8
# __author__ = 'Mio'
import logging

from tornado.web import authenticated
from mongoengine import DoesNotExist, Q

from tools.web.base import BaseRequestHandler, WordHandler
from models.word import Word
from models.record import Record, WORD_FINISHED, WORD_UNDONE


class ReciteWordsHandler(BaseRequestHandler):
    @authenticated
    def get(self):
        """
        生成背诵列表
        使用Cookie来记录用户的Record
        :return:
        """
        user = self.get_current_user_mongo()

        # 获取上次未完成的背诵
        record = self.get_current_record()
        if record:
            # self.write_response(record.format_response())
            next_word = record.next_word
            self.set_secure_cookie("next_word", next_word)
            self.render("recite.html", record=record.format_response(), next_word=next_word)
            return

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
        # 如果有值, 会返回只拥有一个元素的列表
        recited_words = list(recited_words)

        query = [Q(scope__in=[user.scope])]
        if recited_words:
            query.append(Q(word__nin=recited_words[0]['words_recited']))

        query = reduce(lambda x, y: x & y, query)
        # 获取新的待背诵单词
        wait_words = Word.objects(query).limit(user.quota)
        # 记录新的背诵记录
        new_record = Record(
            user=user, words=[{"word": word.word, "status": WORD_UNDONE} for word in wait_words]
        ).save()
        self.set_secure_cookie("record_id", str(new_record.id))
        next_word = new_record.words[0]['word']
        # self.set_secure_cookie("next_word", next_word)
        self.render("recite.html", record=new_record.format_response(), next_word=next_word)
        return


class OneWordReciteHandler(WordHandler):
    @authenticated
    def get(self, word):
        """
        完成一个单词
        :param word:
        :return:
        """
        back_to_word = self.get_argument("back_to", None)
        if back_to_word and back_to_word != word:
            try:
                _word = Word.objects(word=word).get()
            except DoesNotExist as e:
                logging.error(e)
                self.render_word(word_content=None, error="No word found, sorry")
                return
            self.render_word(word_content=_word.format_response(), back_to_word=back_to_word)
            return
        record = self.get_current_record()
        for _word in record.words:
            if _word['word'] == word:
                _word['status'] = WORD_FINISHED
                record.save()
                break

        next_word = record.next_word
        if next_word == "END":
            self.render("end.html")
        else:
            _word = Word.objects(word=record.next_word).get()
            self.render_word(word_content=_word.format_response())


class OneWordHandler(WordHandler):
    @authenticated
    def get(self, word):
        if word == "END":
            self.render("end.html")
            return

        back_to_word = self.get_argument("back_to", None)
        if back_to_word and back_to_word != word:
            try:
                _word = Word.objects(word=word).get()
            except DoesNotExist as e:
                logging.error(e)
                # self.render("word.html", word=None, error="No word found, sorry", back_to_word=None)
                self.render_word(error="No word found, sorry")
                return
            # self.render("word.html", word=_word.format_response(), error=None, back_to_word=back_to_word)
            self.render_word(word_content=_word.format_response(), back_to_word=back_to_word)
            return

        try:
            _word = Word.objects(word=word).get()
        except DoesNotExist:
            # self.render("word.html", word=None, error="word '{}' not found, sorry".format(word), back_to_word=None)
            self.render_word(error="word '{}' not found, sorry".format(word))
            return

        logging.info(_word)
        if _word:
            self.render_word(word_content=_word.format_response())
        else:
            self.render_word(error="word {} not found, sorry".format(word))
        return
