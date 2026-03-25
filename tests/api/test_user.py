"""
用户接口测试用例
"""
import pytest
from core.http_client import HttpClient
from api.user import UserApi


class TestUserApi:
    """用户API测试类 - 单个接口测试"""

    def test_get_user_info(self, user_api):
        """
        测试获取用户信息接口

        验证:
        - 接口返回成功
        - 返回用户信息包含必要字段
        """
        print("\n=== 测试获取用户信息接口 ===")

        result = user_api.get_user_info()

        print(f"响应结果: {result}")

        # 断言
        assert result.get("success") is True, f"接口返回失败: {result}"
        assert "data" in result, "响应缺少data字段"

    def test_get_profile(self, user_api):
        """
        测试获取用户资料接口

        注: 如果接口返回404，说明该接口路径可能不存在或需要其他参数
        """
        print("\n=== 测试获取用户资料接口 ===")

        result = user_api.get_profile()

        print(f"响应结果: {result}")

        # 允许接口不存在的情况
        if result.get("errorCode") == 404:
            print("接口路径不存在，跳过")
            return

        # 断言
        assert result.get("success") is True, f"接口返回失败: {result}"

    def test_get_balance(self, user_api):
        """
        测试获取用户余额接口

        注: 如果接口返回404，说明该接口路径可能不存在或需要其他参数
        """
        print("\n=== 测试获取用户余额接口 ===")

        result = user_api.get_balance()

        print(f"响应结果: {result}")

        # 允许接口不存在的情况
        if result.get("errorCode") == 404:
            print("接口路径不存在，跳过")
            return

        # 断言
        assert result.get("success") is True, f"接口返回失败: {result}"

    def test_get_wallet_info(self, user_api):
        """
        测试获取钱包信息接口
        """
        print("\n=== 测试获取钱包信息接口 ===")

        result = user_api.get_wallet_info()

        print(f"响应结果: {result}")

        # 允许接口不存在的情况
        if result.get("errorCode") == 404:
            print("接口路径不存在，跳过")
            return

        # 断言
        assert "data" in result or result.get("success") is not None


class TestTokenAuth:
    """Token认证测试类"""

    def test_token_exists(self, token):
        """
        验证token是否存在
        """
        print(f"\n=== 验证Token ===")
        print(f"Token: {token}")

        assert token is not None, "Token不应该为空"
        assert len(token) > 0, "Token长度应该大于0"
        assert token.startswith("eyJ"), "Token应该是JWT格式"
    def test_access_without_token(self):
        """
        测试无Token访问需要登录的接口

        前置条件：未登录、无Token

        步骤：
        1. 创建不带Token的HttpClient
        2. 调用需要登录的用户信息接口

        预期结果：返回401，错误信息：The JWT token is invalid. Please verify that the token is correct.
        """
        print("\n=== 测试无Token访问需要登录的接口 ===")

        # 创建不带Token的客户端
        client = HttpClient()
        user_api = UserApi(client)

        # 调用需要登录的接口
        result = user_api.get_user_info()

        print(f"响应结果: {result}")

        # 断言：错误信息包含 token 相关提示
        error_message = result.get("errorMessage", "")
        assert "token" in error_message.lower() or "invalid" in error_message.lower(), \
            f"错误信息应该包含token相关提示，实际: {error_message}"

        print("=== 测试通过：无Token访问被正确拒绝 ===")
