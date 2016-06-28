# coding=utf-8
# __author__ = 'Mio'

from handlers import (user_handler, home_page_handler)

urls = [
    (r"/", home_page_handler.HomePageHandler),
]

# 用户
urls += [
    # 获取、创建用户信息
    (r"/user", user_handler.UseHandler),
]