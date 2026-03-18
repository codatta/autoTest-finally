"""
认证模块
处理Web3钱包登录，获取和管理token
"""
from typing import Optional, Dict, Any
from core.signer import Web3Signer, create_signer
from core.http_client import HttpClient, create_client
from config.settings import config


class Auth:
    """认证管理类"""

    def __init__(self, private_key: Optional[str] = None):
        """
        初始化认证

        Args:
            private_key: 钱包私钥
        """
        self.private_key = private_key or config.PRIVATE_KEY
        self.signer: Optional[Web3Signer] = None
        # 创建client时传入重新登录的回调
        self.client: HttpClient = create_client()
        self.client.on_unauthorized = self.relogin
        self.token: Optional[str] = None

    def _get_nonce(self) -> str:
        """
        获取nonce

        Returns:
            nonce字符串

        Raises:
            Exception: 获取nonce失败时抛出
        """
        response = self.client.post(
            "/api/v2/user/nonce",
            json_data={"account_type": "block_chain"}
        )

        if response.status_code != 200:
            raise Exception(f"获取nonce失败: {response.status_code} - {response.text}")

        data = response.json()
        # nonce可能在data字段中，也可能是data本身
        nonce = data.get("data")
        if isinstance(nonce, str):
            return nonce
        return data.get("data", {}).get("nonce", "")

    def login(self) -> str:
        """
        执行登录，获取token

        Returns:
            token字符串

        Raises:
            Exception: 登录失败时抛出
        """
        # 创建签名器
        self.signer = create_signer(self.private_key)

        # 获取nonce
        nonce = self._get_nonce()

        # 签名消息
        sign_result = self.signer.sign_message(
            domain=config.BASE_URL,
            nonce=nonce
        )

        # 构建登录请求参数
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

        # 调用登录接口
        response = self.client.post("/api/v2/user/login", json_data=login_data)

        if response.status_code != 200:
            raise Exception(f"登录失败: {response.status_code} - {response.text}")

        data = response.json()
        token = data.get("data", {}).get("token", "")

        if not token:
            raise Exception(f"登录成功但未获取到token: {response.text}")

        # 保存token到客户端
        self.token = token
        self.client.set_token(token)

        return token

    def get_token(self) -> Optional[str]:
        """获取当前token"""
        return self.token

    def set_token(self, token: str):
        """设置token"""
        self.token = token
        self.client.set_token(token)

    def relogin(self) -> str:
        """
        重新登录，获取新token

        Returns:
            新的token字符串
        """
        print(f"\n=== Token可能已过期，重新登录获取新token ===")
        token = self.login()
        print(f"=== 重新登录成功，token: {token[:50]}... ===")
        return token

    def get_client(self) -> HttpClient:
        """获取HTTP客户端（已设置token）"""
        return self.client


def create_auth(private_key: Optional[str] = None) -> Auth:
    """
    创建认证实例工厂函数

    Args:
        private_key: 私钥

    Returns:
        Auth实例
    """
    return Auth(private_key=private_key)
