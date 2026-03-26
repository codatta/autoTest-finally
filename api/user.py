"""
用户相关API接口
"""
from typing import Dict, Any, Optional
from core.http_client import HttpClient


class UserApi:
    """用户API"""

    def __init__(self, client: HttpClient):
        self.client = client

    def get_user_info(self) -> Dict[str, Any]:
        """
        获取用户信息

        Returns:
            API响应数据
        """
        response = self.client.post("/api/v2/user/get/user_info")
        return response.json()

    def get_profile(self) -> Dict[str, Any]:
        """
        获取用户资料

        Returns:
            API响应数据
        """
        response = self.client.post("/api/v2/user/get/profile")
        return response.json()

    def get_balance(self) -> Dict[str, Any]:
        """
        获取用户余额

        Returns:
            API响应数据
        """
        response = self.client.get("/api/v2/user/balance")
        return response.json()

    def get_wallet_info(self) -> Dict[str, Any]:
        """
        获取钱包信息

        Returns:
            API响应数据
        """
        response = self.client.get("/api/v2/user/wallet/info")
        return response.json()

    def update_user_info(self, update_key: str, update_value: str) -> Dict[str, Any]:
        """
        更新用户信息

        Args:
            update_key: 更新字段（如 USER_NAME, AVATAR 等）
            update_value: 更新值

        Returns:
            API响应数据
        """
        payload = {
            "update_key": update_key,
            "update_value": update_value
        }
        response = self.client.post("/api/v2/user/update/info", json_data=payload)
        return response.json()
