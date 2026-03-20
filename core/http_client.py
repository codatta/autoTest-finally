"""
HTTP客户端模块
封装requests库，提供简洁的API调用方式
"""
import time
import requests
from typing import Optional, Dict, Any, Callable
from config.settings import config


class HttpClient:
    """HTTP客户端"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        auth: Optional[Any] = None,
        on_unauthorized: Optional[Callable[[], str]] = None
    ):
        """
        初始化HTTP客户端

        Args:
            base_url: 基础URL
            token: 认证token
            auth: Auth实例，用于token过期时重新登录
            on_unauthorized: token过期时的回调函数，返回新token
        """
        self.base_url = base_url or config.get_base_url()
        self.session = requests.Session()
        self.token = token
        self.auth = auth
        self.on_unauthorized = on_unauthorized

    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        获取请求头

        Args:
            additional_headers: 额外的请求头

        Returns:
            合并后的请求头字典
        """
        # 动态获取当前 BASE_URL
        base_url = config.get_base_url()

        # 动态生成请求头
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json",
            "origin": base_url,
            "referer": f"{base_url}/account/signin?from=%2Fapp",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "device": config.DEVICE,
            "channel": config.CHANNEL,
        }

        # 添加token
        if self.token:
            headers["token"] = self.token

        # 合并额外请求头
        if additional_headers:
            headers.update(additional_headers)

        return headers

    def set_token(self, token: str):
        """设置token"""
        self.token = token

    def get_token(self) -> Optional[str]:
        """获取token"""
        return self.token

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retry_on_unauthorized: bool = True,
        **kwargs
    ) -> requests.Response:
        """
        发送HTTP请求

        Args:
            method: HTTP方法
            path: 请求路径
            params: URL参数
            json_data: JSON请求体
            headers: 额外请求头
            retry_on_unauthorized: 是否在token过期时自动重新登录重试
            **kwargs: 其他传递给requests的参数

        Returns:
            Response对象
        """
        url = f"{self.base_url}{path}"
        request_headers = self._get_headers(headers)

        # 每次请求前等待 1 秒，避免频率限制
        time.sleep(1)

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            headers=request_headers,
            **kwargs
        )

        # 如果收到401且启用自动重试，则重新登录后重试
        if response.status_code == 401 and retry_on_unauthorized:
            if self.on_unauthorized:
                # 调用回调重新登录获取新token
                new_token = self.on_unauthorized()
                self.token = new_token
                self.set_token(new_token)

                # 重新发送请求前等待 1 秒
                time.sleep(1)
                request_headers = self._get_headers(headers)
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=request_headers,
                    **kwargs
                )

        return response

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request("GET", path, params=params, **kwargs)

    def post(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """POST请求"""
        return self.request("POST", path, params=params, json_data=json_data)

    def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """PUT请求"""
        return self.request("PUT", path, json_data=json_data)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request("DELETE", path, **kwargs)


def create_client(base_url: Optional[str] = None, token: Optional[str] = None) -> HttpClient:
    """
    创建HTTP客户端工厂函数

    Args:
        base_url: 基础URL
        token: token

    Returns:
        HttpClient实例
    """
    return HttpClient(base_url=base_url, token=token)
