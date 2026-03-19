"""
签到相关API接口
"""
from typing import Dict, Any
from core.http_client import HttpClient


class CheckInApi:
    """签到API"""

    def __init__(self, client: HttpClient):
        self.client = client

    def consult(self) -> Dict[str, Any]:
        """
        查询当天是否已签到

        Returns:
            API响应数据
        """
        response = self.client.post("/api/v2/check-in/consult")
        return response.json()
