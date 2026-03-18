"""
Frontier相关API接口
"""
from typing import Dict, Any, Optional
from core.http_client import HttpClient


class FrontierApi:
    """Frontier API"""

    def __init__(self, client: HttpClient):
        self.client = client

    def list(self, channel: str = "") -> Dict[str, Any]:
        """
        获取frontier列表

        Args:
            channel: 渠道标识

        Returns:
            API响应数据
        """
        response = self.client.post(
            "/api/v2/frontier/list",
            json_data={"channel": channel}
        )
        return response.json()
