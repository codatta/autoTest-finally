"""
响应断言工具
提供简洁的断言方法
"""
from typing import Any, Dict
import json


class ResponseAssert:
    """响应断言类"""

    def __init__(self, response):
        """
        初始化

        Args:
            response: requests.Response对象
        """
        self.response = response
        self.data = response.json() if response.content else {}

    def status_code(self, code: int):
        """断言状态码"""
        assert self.response.status_code == code, \
            f"状态码期望: {code}, 实际: {self.response.status_code}, 响应: {self.data}"
        return self

    def success(self, expect_success: bool = True):
        """断言是否成功"""
        actual_success = self.data.get("success", False)
        assert actual_success == expect_success, \
            f"success期望: {expect_success}, 实际: {actual_success}, 响应: {self.data}"
        return self

    def code(self, expect_code: int):
        """断言code"""
        actual_code = self.data.get("code", -1)
        assert actual_code == expect_code, \
            f"code期望: {expect_code}, 实际: {actual_code}, 响应: {self.data}"
        return self

    def has_key(self, key: str):
        """断言响应包含某个key"""
        assert key in self.data, \
            f"响应不包含key: {key}, 响应: {self.data}"
        return self

    def has_data_key(self, key: str):
        """断言响应data中包含某个key"""
        data = self.data.get("data", {})
        assert key in data, \
            f"响应data不包含key: {key}, 响应: {self.data}"
        return self

    def equals(self, key: str, value: Any):
        """断言某个key的值等于指定值"""
        actual = self.data.get(key)
        assert actual == value, \
            f"key={key} 期望: {value}, 实际: {actual}, 响应: {self.data}"
        return self

    def data_equals(self, key: str, value: Any):
        """断言data中某个key的值等于指定值"""
        data = self.data.get("data", {})
        actual = data.get(key)
        assert actual == value, \
            f"data.{key} 期望: {value}, 实际: {actual}, 响应: {self.data}"
        return self

    def not_empty(self, key: str):
        """断言某个key的值不为空"""
        value = self.data.get(key)
        assert value, f"key={key} 不能为空, 响应: {self.data}"
        return self

    def data_not_empty(self, key: str):
        """断言data中某个key的值不为空"""
        data = self.data.get("data", {})
        value = data.get(key)
        assert value, f"data.{key} 不能为空, 响应: {self.data}"
        return self


def assert_response(response, **kwargs):
    """
    快速断言辅助函数

    Args:
        response: requests.Response对象
        **kwargs: 断言条件

    Returns:
        ResponseAssert实例
    """
    assert_obj = ResponseAssert(response)

    if "status_code" in kwargs:
        assert_obj.status_code(kwargs["status_code"])

    if "success" in kwargs:
        assert_obj.success(kwargs["success"])

    if "code" in kwargs:
        assert_obj.code(kwargs["code"])

    return assert_obj
