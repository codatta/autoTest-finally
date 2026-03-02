# utils/web3_utils.py
# Web3 / Ethereum 签名工具封装（使用 eth-account）
# 提供从私钥生成地址和对消息签名的简单函数。

from eth_account import Account
from eth_account.messages import encode_defunct


def address_from_private_key(private_key: str) -> str:
    """根据私钥返回以太坊地址（0x 开头的小写/校验和地址）。"""
    acct = Account.from_key(private_key)
    return acct.address


def sign_message_hex(private_key: str, message: str) -> str:
    """
    对任意文本消息进行 "Ethereum Signed Message" 签名，并返回十六进制签名字符串（0x...）。

    注意：如果后端使用 SIWE/EIP-4361 标准，message 应当为 SIWE 格式的字符串。
    """
    acct = Account.from_key(private_key)
    msg = encode_defunct(text=message)
    signed = acct.sign_message(msg)
    # 返回 0x 开头的签名字符串
    return signed.signature.hex()

