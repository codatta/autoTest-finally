# core/http_client.py
# 轻量 HTTP 客户端封装：基于 requests.Session，提供统一的超时、基础 URL 处理和简易请求方法。

import requests


class APIClient:
    """
    简单的 HTTP 客户端封装类。

    参数：
    - base_url: API 根地址（例如 https://api.example.com）
    - timeout: 请求超时时间（秒）

    用法示例：
        client = APIClient(base_url="https://api.example.com", timeout=5)
        resp = client.get('/health')
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 10):
        # 规范化 base_url，移除末尾斜杠
        self.base_url = base_url.rstrip('/')
        # 使用 requests 的 Session 以便复用连接
        self.session = requests.Session()
        self.timeout = timeout

    def _url(self, path: str) -> str:
        """根据传入的相对路径构造完整 URL。"""
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs):
        """
        发起 GET 请求，返回 requests.Response 对象。
        额外的 requests 参数（如 params、headers）可通过 kwargs 传入。
        """
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        """
        发起 POST 请求，默认以 JSON body 发送（传入 json 参数）。
        额外参数（如 headers）可通过 kwargs 传入。
        """
        return self.session.post(self._url(path), json=json, timeout=self.timeout, **kwargs)
