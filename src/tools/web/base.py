# coding=utf-8
# __author__ = 'Mio'

import ujson as json

import tornado.web

from tools.web.error_code import ERR_UNKNOWN, ERR_NO_CONTENT, ERR_MULTIPLE_OBJ_RETURNED, ERR_DUPLICATE_ENTRY, ERR_ARG
from tools.web.http_code import (HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST,
                                 HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN)
from models.user import User
from bson import ObjectId


class BaseRequestHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        user_id = self.get_secure_cookie("shanbay_user")
        if not user_id:
            return None
        user = User.objects(pk=ObjectId(user_id)).get()
        return user.name


    def get_query_args(self):
        """
        获取query_arguments，同一key有重复值时只取值列表最后一个
        :return:
        """
        return {key: value[-1] for key, value in self.request.query_arguments.iteritems()}

    def get_body_args(self):
        """
        获取body_arguments, 只取列表最后一个
        :return:
        """
        if self.request.body:
            return json.loads(self.request.body)
        if self.request.body_arguments:
            return {key: value[-1] for key, value in self.request.body_arguments.iteritems()}
        return {}

        # def options(self):
        #     self.set_header("Access-Control-Allow-Origin", "*")
        #     self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        #     self.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        # pass

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get("Origin"))
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1728000)
        self.set_header('Access-Control-Allow-Headers', 'CONTENT-TYPE, Access-Control-Allow-Origin,x-access-token')

    def write_response(self, content=None, error_code=0, message="",
                       status_code=HTTP_200_OK, reason=None, headers=None, clear=False):
        if clear:
            self.clear()
        if headers is None:
            headers = {}
        _headers = {
            "Access-Control-Allow-Origin": self.request.headers.get("Origin", ''),
            'Access-Control-Allow-Methods': 'POST, GET, PUT, DELETE, OPTIONS',
            # "Access-Control-Max-Age": 1728000,
            # 'Cache-Control': "no-cache",
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Access-Control-Expose-Headers': 'X-Resource-Count',
            'Access-Control-Allow-Headers': 'CONTENT-TYPE, Access-Control-Allow-Origin,x-access-token'
        }
        headers.update(_headers)
        self.set_headers(headers)
        self.set_status(status_code, reason=reason)
        if status_code != HTTP_204_NO_CONTENT:
            # 如果是204的返回, http的标准是不能有body, 所以tornado的httpclient接收的时候会
            # 报错变成599错误
            self.write(dict(error_code=error_code, message=message, data=content))

    def write_error_response(self, content=None, error_code=ERR_UNKNOWN, message="UnknownError",
                             status_code=HTTP_200_OK, reason=None):
        """
        错误响应
        :param error_code:
        :param message:
        :param status_code:
        :param content:
        :param reason:
        :return:
        """
        self.clear()
        if status_code == HTTP_422_UNPROCESSABLE_ENTITY and not reason:
            reason = message
        self.write_response(content=content, error_code=error_code, message=message,
                            status_code=status_code, reason=reason)

    def write_no_content_response(self):
        self.set_status(HTTP_204_NO_CONTENT)

    def write_not_found_entity_response(self, content=None, message="没有找到对应实体"):
        """
        查询id没有结果
        :param message:
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=ERR_NO_CONTENT, message=message,
                                  status_code=HTTP_400_BAD_REQUEST)

    def write_multiple_results_found_response(self, content=None):
        """
        查询获取单个数据时，找到不止一个
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=ERR_MULTIPLE_OBJ_RETURNED,
                                  message="MultipleObjectsReturned",
                                  status_code=HTTP_400_BAD_REQUEST)

    def write_unprocessable_entity_response(self, content=None):
        """
        创建中的错误
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=ERR_UNKNOWN, message="UNPROCESSABLE_ENTITY",
                                  status_code=HTTP_400_BAD_REQUEST, reason="UNPROCESSABLE_ENTITY")

    def write_parse_args_failed_response(self, message="args parse failed", content=None):
        """
        参数解析错误
        :param message:
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=ERR_ARG, message=message,
                                  status_code=HTTP_400_BAD_REQUEST)

    def write_duplicate_entry_response(self, content=None, message="Duplicate entry"):
        """
        插入操作，重复键值
        :param message:
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=ERR_DUPLICATE_ENTRY, message=message,
                                  status_code=HTTP_400_BAD_REQUEST, reason="Duplicate entry")

    def write_unauthorized(self, content=None, message="Unauthorized"):
        """
        身份验证失败
        :param content:
        :param message:
        :return:
        """
        self.write_error_response(content=content, error_code=110, message=message, status_code=HTTP_401_UNAUTHORIZED)

    def write_forbidden_response(self, content=None, message="Forbidden"):
        """
        被禁止
        :param message:
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=107, message=message,
                                  status_code=HTTP_403_FORBIDDEN)

    def set_headers(self, headers):
        # type: (dict) -> None
        if headers:
            for header in headers:
                self.set_header(header, headers[header])
