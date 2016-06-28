# coding=utf-8
# __author__ = 'Mio'

import os

SETTINGS = {
    "debug": True,
    "autoreload": True,
    "cookie_secret": "dcc8902e-d4f0-4951-a660-6bcaae23a6aa",
    "login_url": "/login",
    # "xsrf_cookies": True,
    # "template_path": os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui/dist/"),
    # "static_path": os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui/dist/"),
    # "static_url_prefix": "/ui/",
    "xsrf_cookies": False,
    "template_path": os.path.join(os.path.dirname(__file__), os.pardir, "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), os.pardir, "static"),
}
