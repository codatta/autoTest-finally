# api/wallet_api.py
# 钱包模块占位示例：封装钱包/余额相关接口。

from api_test_framework.api.base_api import BaseAPI


class WalletAPI(BaseAPI):
    """钱包 API 示例：提供获取用户余额的接口封装。"""

    def get_balance(self, user_id):
        """根据用户 ID 获取钱包余额（示例路径），返回 requests.Response。"""
        return self.get(f"/wallets/{user_id}/balance")
