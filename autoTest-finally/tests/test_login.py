"""
登录流程测试
"""
import pytest
from core.auth import Auth
from core.http_client import HttpClient
from api.user import UserApi
from config.settings import config


class TestLogin:
    """登录流程测试类"""

    def test_login_flow(self):
        """
        测试完整的登录流程

        流程:
        1. 创建Auth实例
        2. 调用login方法获取token
        3. 使用token调用用户信息接口验证
        """
        print("\n=== 测试完整登录流程 ===")

        # 1. 创建Auth实例，使用提供的私钥
        private_key = "0x40e68d7c277fbbd3399e7568011ec02cdb5f1009c1db15d883ef51bb41deb028"
        auth = Auth(private_key=private_key)

        # 2. 登录获取token
        token = auth.login()

        print(f"获取到的Token: {token[:50]}...")

        # 3. 验证token格式
        assert token is not None
        assert len(token) > 0
        assert token.startswith("eyJ")  # JWT token以eyJ开头

        # 4. 使用token获取客户端
        client = auth.get_client()

        # 5. 调用用户信息接口验证
        response = client.post("/api/v2/user/get/user_info")
        result = response.json()

        print(f"用户信息响应: {result}")

        # 6. 断言
        assert response.status_code == 200, f"请求失败: {response.status_code}"
        assert result.get("success") is True, f"接口返回失败: {result}"

    def test_nonce_api(self):
        """
        测试nonce接口
        """
        print("\n=== 测试Nonce接口 ===")

        client = HttpClient()
        response = client.post("/api/v2/user/nonce", json_data={"account_type": "block_chain"})

        result = response.json()

        print(f"Nonce响应: {result}")

        assert response.status_code == 200
        assert result.get("success") is True
        assert "data" in result


    def test_wallet_signature(self):
        """
        测试签名功能
        """
        print("\n=== 测试钱包签名 ===")

        from core.signer import Web3Signer

        private_key = "0x40e68d7c277fbbd3399e7568011ec02cdb5f1009c1db15d883ef51bb41deb028"
        signer = Web3Signer(private_key)

        print(f"钱包地址: {signer.address}")

        # 测试签名
        sign_result = signer.sign_message(
            domain="https://app-test.b18a.io",
            nonce="test_nonce_123"
        )

        print(f"签名结果:")
        print(f"  - address: {sign_result['address']}")
        print(f"  - signature: {sign_result['signature'][:50]}...")
        print(f"  - message: {sign_result['message'][:100]}...")

        # 验证签名
        assert sign_result["address"] is not None
        assert sign_result["signature"] is not None
        assert sign_result["message"] is not None
