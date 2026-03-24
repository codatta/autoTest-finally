"""
登录认证场景测试用例

包含以下场景：
- 完整登录流程（登录 → 验证token → 调用受保护接口）
"""
import pytest
import os
from core.auth import Auth
from api.user import UserApi


class TestLoginFlow:
    """登录认证流程场景测试"""

    def test_complete_login_flow(self):
        """
        【场景测试】完整登录流程

        步骤：
        1. 创建Auth实例并登录
        2. 获取token
        3. 使用token调用用户信息接口验证

        验证:
        - 登录成功获取有效token
        - 使用token可以正常调用受保护接口
        """
        print("\n=== 【场景测试】完整登录流程 ===")

        # 从环境变量获取私钥
        private_key = os.getenv("PRIVATE_KEY")
        assert private_key, "PRIVATE_KEY 环境变量未设置"

        # --- 步骤 1: 创建Auth实例并登录 ---
        print("\n步骤1: 创建Auth实例并登录...")
        auth = Auth(private_key=private_key)
        token = auth.login()
        print(f"登录成功，获取token: {token[:50]}...")

        # 验证token格式
        assert token is not None, "Token不能为空"
        assert token.startswith("eyJ"), "Token应该是JWT格式"

        # --- 步骤 2: 获取token ---
        print("\n步骤2: 获取token...")
        stored_token = auth.get_token()
        assert stored_token == token, "存储的token与返回的token不一致"

        # --- 步骤 3: 使用token验证登录 ---
        print("\n步骤3: 使用token获取用户信息...")
        client = auth.get_client()
        user_api = UserApi(client)
        result = user_api.get_user_info()
        print(f"用户信息响应: {result}")

        assert result.get("success") is True, f"获取用户信息失败: {result}"

        print("=== 场景测试通过：完整登录流程验证成功 ===")
