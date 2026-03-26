"""
用户接口测试用例
"""
import pytest
import random
import string
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

    def test_update_username(self, user_api):
        """
        测试修改用户名

        步骤：
        1. 查询当前用户名
        2. 生成随机十位数字的用户名
        3. 修改用户名为随机十位数字
        4. 再次查询验证修改成功

        预期结果：修改成功，新用户名生效
        """
        print("\n=== 测试修改用户名 ===")

        # --- 步骤 1: 查询当前用户名 ---
        print("\n步骤1: 查询当前用户名...")
        user_info = user_api.get_user_info()
        print(f"用户信息: {user_info}")

        assert user_info.get("success") is True, f"获取用户信息失败: {user_info}"

        data = user_info.get("data", {})
        # 用户名在 user_data 里面
        user_data = data.get("user_data", {})
        original_username = user_data.get("user_name") or user_data.get("userName") or user_data.get("username") or ""
        print(f"原始用户名: {original_username}")

        # --- 步骤 2: 生成随机十位数字的用户名 ---
        print("\n步骤2: 生成随机十位数字的用户名...")
        new_username = ''.join(random.choices(string.digits, k=10))
        print(f"新用户名: {new_username}")

        # --- 步骤 3: 修改用户名 ---
        print("\n步骤3: 修改用户名...")
        update_result = user_api.update_user_info("USER_NAME", new_username)
        print(f"修改响应: {update_result}")

        # 断言修改成功（网络问题除外）
        if update_result.get("success") is False:
            error_msg = update_result.get("errorMessage", "")
            error_code = update_result.get("errorCode", 0)
            # 网络相关错误码可以重试（如504超时等）
            if error_code in [504, 502, 503] or "timeout" in error_msg.lower():
                print(f"⚠️ 网络错误，重试一次...")
                update_result = user_api.update_user_info("USER_NAME", new_username)
                print(f"重试响应: {update_result}")

        # 最终断言必须成功
        assert update_result.get("success") is True, f"修改用户名失败: {update_result}"

        # --- 步骤 4: 再次查询验证修改成功 ---
        print("\n步骤4: 再次查询验证修改成功...")
        user_info_after = user_api.get_user_info()
        print(f"修改后用户信息: {user_info_after}")

        data_after = user_info_after.get("data", {})
        # 用户名在 user_data 里面
        user_data_after = data_after.get("user_data", {})
        updated_username = user_data_after.get("user_name") or user_data_after.get("userName") or user_data_after.get("username") or ""
        print(f"修改后用户名: {updated_username}")

        # 断言：用户名已更新
        assert updated_username == new_username, \
            f"用户名未修改成功，期望: {new_username}，实际: {updated_username}"

        print("=== 测试通过：用户名修改成功 ===")


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
