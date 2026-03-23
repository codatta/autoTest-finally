"""
配置管理模块
从环境变量读取配置，支持多环境切换
"""
import os
from typing import Optional

# 加载.env文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """配置类"""

    # 环境配置
    ENV = os.getenv("TEST_ENV", "test")

    # 域名配置
    BASE_URL = os.getenv("BASE_URL", "https://app-test.b18a.io")

    # 报告配置
    MAX_REPORT_COUNT = int(os.getenv("MAX_REPORT_COUNT", "30"))  # 报告保留数量

    # 邮件配置
    EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")  # 发件人邮箱
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")  # 邮箱密码/授权码
    EMAIL_FROM = os.getenv("EMAIL_FROM", "")  # 发件人名称
    EMAIL_TO = os.getenv("EMAIL_TO", "")  # 收件人，多个用逗号分隔

    # 区块链配置
    CHAIN_ID = os.getenv("CHAIN_ID", "56")  # BSC链
    CHAIN = os.getenv("CHAIN", "56")

    # 钱包配置
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    WALLET_NAME = os.getenv("WALLET_NAME", "OKX Wallet")
    CONNECTOR = os.getenv("CONNECTOR", "codatta_wallet")

    # 设备信息
    DEVICE = os.getenv("DEVICE", "WEB")
    CHANNEL = os.getenv("CHANNEL", "codatta-platform-website")
    APP = os.getenv("APP", "codatta-platform-website")

    # 请求头配置
    DEFAULT_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": BASE_URL,
        "referer": f"{BASE_URL}/account/signin?from=%2Fapp",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }

    @classmethod
    def get_base_url(cls) -> str:
        """获取基础URL"""
        print(f"基础URL: {cls.BASE_URL}")
        return cls.BASE_URL

    @classmethod
    def update_base_url(cls, url: str):
        """更新基础URL"""
        cls.BASE_URL = url
        cls.DEFAULT_HEADERS["origin"] = url
        cls.DEFAULT_HEADERS["referer"] = f"{url}/account/signin?from=%2Fapp"


# 全局配置实例
config = Config()
