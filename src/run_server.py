# coding=utf-8
# __author__ = 'Mio'
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.log import app_log
from tornado.options import define, options, parse_command_line

from uri import uris
from settings.app_setting import SETTINGS
from settings.mongo_setting import MONGODB_NAME, MONGODB_CONFIG
from mongoengine import connect

define("port", default=5555, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        # 连接MongoDB
        connect(MONGODB_NAME, **MONGODB_CONFIG)
        tornado.web.Application.__init__(self, uris, **SETTINGS)


application = Application()

if __name__ == "__main__":
    parse_command_line()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    app_log.info("run on port:{}".format(options.port))
    io_loop_ = tornado.ioloop.IOLoop.current()
    io_loop_.start()
