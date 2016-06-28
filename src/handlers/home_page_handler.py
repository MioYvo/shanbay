# coding=utf-8
# __author__ = 'Mio'

from tools.web.base import BaseRequestHandler


class HomePageHandler(BaseRequestHandler):
    def get(self):
        self.write_response("welcome {}".format(self.current_user))

    def post(self):
        pass
