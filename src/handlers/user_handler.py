# coding=utf-8
# __author__ = 'Mio'
import logging

from schema import Schema, Use

from models.user import User
from tools.web.base import BaseRequestHandler
from tools.web.escape import schema_utf8


class UseHandler(BaseRequestHandler):
    # 获取用户信息
    def get(self):
        self.write_response(content=[user.format_response() for user in User.objects()])

    # 注册用户
    def post(self):
        data = self.post_schema()
        if not data:
            return

        # 判断重复
        if User.objects(name=data['name']).all():
            self.write_duplicate_entry_response(content="name: {}".format(data['name']))
            return

        # 存储
        new_user = User(name=data['name'], scope=data['scope'], quota=data['quota']).save()
        self.write_response(content=new_user.format_response())

    def post_schema(self):
        try:
            data = Schema({
                "name": schema_utf8,
                "scope": schema_utf8,
                "quota": Use(int)
            }).validate(self.get_body_args())
        except Exception as e:
            logging.error(e)
            self.write_parse_args_failed_response(content=e.message)
            return False
        else:
            return data

    # 修改用户
    def put(self):
        pass

    # 修改用户属性
    def patch(self):
        pass

    # 删除用户
    def delete(self):
        pass
