"""
登录认证场景测试用例

包含以下场景：
- 完整登录流程（登录 → 验证token → 调用受保护接口）
- 登录流程（异常场景-非法私钥）
- 登录流程（边界场景-过期nonce）
"""
import pytest
import os
from eth_account import Account
from core.auth import Auth
from core.signer import create_signer
from core.http_client import create_client
from config.settings import config
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

    def test_login_with_invalid_private_key(self):
        """
        【场景测试】登录流程（异常场景-非法私钥）

        思路：用私钥A签名，但把地址篡改为私钥B的地址，模拟签名与地址不匹配，
        服务端签名校验应失败。

        步骤：
        1. 生成两个随机私钥A和B
        2. 用私钥A获取nonce并签名
        3. 将签名结果中的地址替换为私钥B的地址
        4. 调用登录接口，预期签名校验失败

        验证:
        - 登录接口返回success=False
        - 未返回有效Token
        """
        print("\n=== 【场景测试】登录流程（异常场景-非法私钥） ===")

        # --- 步骤 1: 生成两个随机私钥 ---
        print("\n步骤1: 生成两个随机私钥...")
        account_a = Account.create()
        account_b = Account.create()
        print(f"私钥A钱包地址: {account_a.address}")
        print(f"私钥B钱包地址: {account_b.address}")

        # --- 步骤 2: 用私钥A获取nonce并签名 ---
        print("\n步骤2: 用私钥A获取nonce并签名...")
        client = create_client()
        signer_a = create_signer(account_a.key.hex())

        # 获取nonce
        response = client.post("/api/v2/user/nonce", json_data={"account_type": "block_chain"})
        nonce_data = response.json()
        nonce = nonce_data.get("data") if isinstance(nonce_data.get("data"), str) else nonce_data.get("data", {}).get("nonce", "")
        print(f"获取nonce: {nonce}")

        # 用私钥A签名
        sign_result = signer_a.sign_message(domain=config.BASE_URL, nonce=nonce)
        print(f"签名完成，原始地址: {sign_result['address']}")

        # --- 步骤 3: 篡改地址为私钥B的地址 ---
        print("\n步骤3: 篡改地址为私钥B的地址（签名与地址不匹配）...")
        tampered_address = account_b.address
        print(f"篡改后地址: {tampered_address}")

        login_data = {
            "account_type": "block_chain",
            "account_enum": "C",
            "connector": config.CONNECTOR,
            "inviter_code": "",
            "wallet_name": config.WALLET_NAME,
            "address": tampered_address,
            "chain": config.CHAIN,
            "nonce": sign_result["nonce"],
            "signature": sign_result["signature"],
            "message": sign_result["message"],
            "source": {
                "device": config.DEVICE,
                "channel": config.CHANNEL,
                "app": config.APP
            }
        }

        # --- 步骤 4: 调用登录接口，预期失败 ---
        print("\n步骤4: 调用登录接口，预期签名校验失败...")
        response = client.post("/api/v2/user/login", json_data=login_data)
        result = response.json()
        print(f"登录响应: {result}")

        assert result.get("success") is False, f"签名与地址不匹配时登录应失败，实际响应: {result}"

        token = result.get("data", {}).get("token") if isinstance(result.get("data"), dict) else None
        assert not token, "签名与地址不匹配时不应返回Token"

        print(f"登录失败，错误信息: {result.get('errorMessage')}")
        print("=== 场景测试通过：非法私钥登录验证成功 ===")

    def test_login_with_expired_nonce(self):
        """
        【场景测试】登录流程（边界场景-过期nonce）

        思路：使用一个伪造的nonce字符串进行签名和登录，
        服务端找不到该nonce记录，等价于nonce已过期/无效。

        步骤：
        1. 获取合法私钥
        2. 构造一个伪造的过期nonce
        3. 用合法私钥对伪造nonce签名
        4. 调用登录接口，预期失败

        验证:
        - 登录接口返回success=False
        - 未返回有效Token
        """
        print("\n=== 【场景测试】登录流程（边界场景-过期nonce） ===")

        # --- 步骤 1: 获取合法私钥 ---
        print("\n步骤1: 获取合法私钥...")
        private_key = os.getenv("PRIVATE_KEY")
        assert private_key, "PRIVATE_KEY 环境变量未设置"

        # --- 步骤 2: 构造伪造的过期nonce ---
        print("\n步骤2: 构造伪造的过期nonce...")
        fake_nonce = "expired_nonce_00000000000000"
        print(f"伪造nonce: {fake_nonce}")

        # --- 步骤 3: 用合法私钥对伪造nonce签名 ---
        print("\n步骤3: 用合法私钥对伪造nonce签名...")
        signer = create_signer(private_key)
        sign_result = signer.sign_message(domain=config.BASE_URL, nonce=fake_nonce)
        print(f"签名完成，地址: {sign_result['address']}")

        login_data = {
            "account_type": "block_chain",
            "account_enum": "C",
            "connector": config.CONNECTOR,
            "inviter_code": "",
            "wallet_name": config.WALLET_NAME,
            "address": sign_result["address"],
            "chain": config.CHAIN,
            "nonce": sign_result["nonce"],
            "signature": sign_result["signature"],
            "message": sign_result["message"],
            "source": {
                "device": config.DEVICE,
                "channel": config.CHANNEL,
                "app": config.APP
            }
        }

        # --- 步骤 4: 调用登录接口，预期失败 ---
        print("\n步骤4: 调用登录接口，预期nonce校验失败...")
        client = create_client()
        response = client.post("/api/v2/user/login", json_data=login_data)
        result = response.json()
        print(f"登录响应: {result}")

        assert result.get("success") is False, f"使用过期nonce登录应失败，实际响应: {result}"

        token = result.get("data", {}).get("token") if isinstance(result.get("data"), dict) else None
        assert not token, "使用过期nonce不应返回Token"

        print(f"登录失败，错误信息: {result.get('errorMessage')}")
        print("=== 场景测试通过：过期nonce登录验证成功 ===")
