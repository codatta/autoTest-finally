"""
Web3签名模块
使用私钥对消息进行签名，支持以太坊风格的消息签名
"""
import json
import time
from eth_account import Account
from eth_account.messages import encode_defunct
from typing import Dict, Any


class Web3Signer:
    """Web3签名器"""

    def __init__(self, private_key: str):
        """
        初始化签名器

        Args:
            private_key: 钱包私钥（带或不带0x前缀均可）
        """
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.address = self.account.address

    def sign_message(self, domain: str, nonce: str) -> Dict[str, Any]:
        """
        签名消息

        Args:
            domain: 域名
            nonce: 从nonce接口获取的nonce值

        Returns:
            包含签名、地址、消息的字典
        """
        # 构造要签名的消息（符合EIP-191标准）
        message = self._create_sign_message(domain, nonce)

        # 对消息进行签名
        message_encoded = encode_defunct(text=message)
        signed = self.account.sign_message(message_encoded)

        return {
            "address": self.address,
            "signature": signed.signature.hex(),
            "message": message,
            "nonce": nonce
        }

    def _create_sign_message(self, domain: str, nonce: str) -> str:
        """
        创建签名消息

        Args:
            domain: 域名
            nonce: nonce值

        Returns:
            格式化的消息字符串
        """
        issued_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

        message = (
            f"{domain} wants you to sign in with your Ethereum account:\n"
            f"{self.address}\n\n"
            f"URI: {domain}/account/signin?from=%2Fapp\n"
            f"Version: 1\n"
            f"Chain ID: 56\n"
            f"Nonce: {nonce}\n"
            f"Issued At: {issued_at}"
        )
        return message


def create_signer(private_key: str) -> Web3Signer:
    """
    创建签名器工厂函数

    Args:
        private_key: 私钥

    Returns:
        Web3Signer实例
    """
    return Web3Signer(private_key)
