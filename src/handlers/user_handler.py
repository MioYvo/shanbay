# coding=utf-8
# __author__ = 'Mio'
import logging

import bcrypt
from tornado.escape import utf8
from mongoengine import DoesNotExist
from tornado.web import authenticated, Finish
from schema import Schema, Use

from models.user import User
from tools.web.base import BaseRequestHandler
from tools.web.escape import schema_utf8
from tools.web.http_code import HTTP_201_CREATED, HTTP_403_FORBIDDEN


class RegisterHandler(BaseRequestHandler):
    def get(self):
        if self.get_current_user():
            # 如果已登录, 则注销
            self.clear_cookie("shanbay_user")
        self.render("register.html")


class UseHandler(BaseRequestHandler):
    # 获取用户信息
    @authenticated
    def get(self):
        print self.current_user
        user = self.get_current_user()
        if not user:
            self.render("/login")
            return
        user = User.objects(name=user).get()
        self.render("user.html", user=user.format_response())

    # 注册用户
    def post(self):
        data = self.post_schema()
        if not data:
            return
        if self.get_current_user():
            self.set_status(status_code=HTTP_403_FORBIDDEN)
            return

        # 判断重复
        if User.objects(name=data['name']).all():
            self.write_duplicate_entry_response(content="name: {}".format(data['name']))
            return

        # 存储
        hashed_password = bcrypt.hashpw(data['password'], bcrypt.gensalt())
        new_user = User(name=data['name'], scope=data['scope'], quota=data['quota'],
                        hashed_password=hashed_password).save()

        self.set_secure_cookie("shanbay_user", str(new_user.id))
        self.render("home.html")
        return
        # self.redirect("/")
        # self.write_response(content=new_user.format_response(), status_code=HTTP_201_CREATED)

    def post_schema(self):
        try:
            data = Schema({
                "name": schema_utf8,
                "scope": schema_utf8,
                "quota": Use(int),
                "password": schema_utf8
            }).validate(self.get_body_args())
        except Exception as e:
            logging.error(e)
            self.write_parse_args_failed_response(content=e.message)
            return False
        else:
            return data

    # 修改用户属性
    def patch(self):
        data = self.patch_schema()
        user = self.get_current_user()

        if user:
            user = User.objects(name=user).get()
        else:
            self.render("/login")
            return

        user.scope = data['scope']
        user.quota = data['quota']
        user.save()
        # self.write_response(content=user.format_response(), status_code=HTTP_201_CREATED)
        self.render("home.html")
        return

    def patch_schema(self):
        try:
            data = Schema({
                "scope": schema_utf8,
                "quota": Use(int)
            }).validate(self.get_body_args())
        except Exception as e:
            logging.error(e)
            self.write_parse_args_failed_response(content=e.message)
            raise Finish
        else:
            return data

    # 删除用户
    def delete(self):
        pass


class LoginHandler(BaseRequestHandler):
    def get(self):
        self.render("login.html", error=None)

    def post_form(self):
        try:
            user = User.objects(name=self.get_argument('name')).get()
        except DoesNotExist:
            self.render("login.html", error="name not found")
            return

        hashed_password = bcrypt.hashpw(utf8(self.get_argument("password")),
                                        utf8(user.hashed_password))
        if hashed_password == user.hashed_password:
            self.set_secure_cookie("shanbay_user", str(user.id))
            self.render("home.html")
            # self.redirect(self.get_argument("next", "/"))
        else:
            logging.error("incorrect password")
            self.render("login.html", error="incorrect password")

    def post(self):
        data = self.post_schema()
        name = data['name']
        password = data['password']
        try:
            user = User.objects(name=name).get()
        except DoesNotExist:
            # 失败
            self.write_not_found_entity_response()
            # self.render("login.html", error="name not found")
            return

        hashed_password = bcrypt.hashpw(utf8(password),
                                        utf8(user.hashed_password))
        if hashed_password == user.hashed_password:
            # 成功
            self.set_secure_cookie("shanbay_user", str(user.id))
            self.write_response(user.format_response())
            return
            # self.render("home.html")
            # self.redirect(self.get_argument("next", "/"))
        else:
            logging.error("incorrect password")
            self.render("login.html", error="incorrect password")
            return

    def post_schema(self):
        try:
            data = Schema({
                "name": schema_utf8,
                "password": schema_utf8
            }).validate(self.get_body_args())
        except Exception as e:
            logging.error(e)
            self.write_parse_args_failed_response(content=e.message)
            raise Finish
        else:
            return data


class LogoutHandler(BaseRequestHandler):
    def get(self):
        self.clear_cookie("shanbay_user")
        self.clear_cookie("record_id")
        self.render("home.html")
        # self.redirect(self.get_argument("next", "/"))
