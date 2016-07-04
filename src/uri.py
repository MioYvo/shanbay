# coding=utf-8
# __author__ = 'Mio'

from handlers import (user_handler, home_page_handler, words_handler, note_handler)

uris = [
    (r"/", home_page_handler.HomePageHandler),
]

# 用户
uris += [
    (r"/login", user_handler.LoginHandler),
    (r"/logout", user_handler.LogoutHandler),
    # 获取、创建用户信息
    (r"/user", user_handler.UseHandler),
    (r"/register", user_handler.RegisterHandler),
]

# 单词
uris += [
    # 背单词
    (r"/words/recite", words_handler.ReciteWordsHandler),
    (r"/words/recite/(.+)", words_handler.OneWordReciteHandler),
    # 单词页面
    (r"/word/details/(.+)", words_handler.OneWordHandler),

]

# 笔记
uris += [
    (r"/word/(.+)/note", note_handler.OneWordNoteHandler),
]
