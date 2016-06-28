# coding=utf-8
# __author__ = 'Mio'
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.log import app_log
from tornado.options import define, options, parse_command_line

from uri import urls
from settings.app_setting import SETTINGS
from settings.mongo_setting import MONGODB_NAME, MONGODB_CONFIG
from mongoengine import connect

define("port", default=5555, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        connect(MONGODB_NAME, **MONGODB_CONFIG)
        tornado.web.Application.__init__(self, urls, **SETTINGS)

application = Application()


if __name__ == "__main__":
    parse_command_line()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    app_log.info("run on port:{}".format(options.port))
    io_loop_ = tornado.ioloop.IOLoop.current()
    io_loop_.start()
