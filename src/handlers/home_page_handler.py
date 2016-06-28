# coding=utf-8
# __author__ = 'Mio'

from tools.web.base import BaseRequestHandler


class HomePageHandler(BaseRequestHandler):
    def get(self):
        self.write_response("welcome")

    def post(self):
        pass
