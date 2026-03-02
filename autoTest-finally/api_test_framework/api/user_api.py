from api_test_framework.api.base_api import BaseAPI

class UserAPI(BaseAPI):
    """User API 示例类：包含获取用户和创建用户的简易封装。"""

    def get_user(self, user_id):
        """根据用户 ID 获取用户信息，返回 requests.Response。"""
        return self.get(f"/users/{user_id}")

    def create_user(self, payload: dict):
        """创建用户（示例）：将 payload 作为 JSON 发送。"""
        return self.post('/users', json=payload)
