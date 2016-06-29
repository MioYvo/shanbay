# coding=utf-8
# __author__ = 'Mio'

from tools.web.base import BaseRequestHandler


class HomePageHandler(BaseRequestHandler):
    def get(self):
        self.render("home.html")

    def post(self):
        pass
