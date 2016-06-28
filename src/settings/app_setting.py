# coding=utf-8
# __author__ = 'Mio'

import os

SETTINGS = {
    "debug": True,
    "autoreload": True,
    # "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    # "template_path": os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui/dist/"),
    "static_path": os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui/dist/"),
    "static_url_prefix": "/ui/",
    "xsrf_cookies": False,
}
