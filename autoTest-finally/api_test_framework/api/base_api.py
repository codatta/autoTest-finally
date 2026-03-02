# api/base_api.py
# 基础 API 类：为业务 API 提供统一的 HTTP 方法封装（GET/POST），并持有一个 APIClient 实例。

from api_test_framework.core.http_client import APIClient


class BaseAPI:
    """
    API 基类：持有 client（APIClient），并封装常见请求方法。

    子类可以继承本类并实现具体业务方法，例如：UserAPI(UserAPI)。
    """

    def __init__(self, base_url: str = None, client: APIClient = None):
        """初始化：可以传入已有的 client（便于测试注入），否则根据 base_url 创建新的 APIClient。"""
        self.client = client or APIClient(base_url=base_url)

    def get(self, path: str, **kwargs):
        """向相对路径发起 GET 请求并返回 Response 对象。"""
        return self.client.get(path, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        """向相对路径发起 POST 请求（JSON body）并返回 Response。"""
        return self.client.post(path, json=json, **kwargs)
