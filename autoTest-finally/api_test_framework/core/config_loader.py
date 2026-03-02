# core/config_loader.py
# 配置加载器：轻量实现，直接从环境变量或 .env 文件加载配置，返回一个简单的对象。

import os
from types import SimpleNamespace
from dotenv import load_dotenv


# 尝试加载仓库中 config/.env 文件（如果存在），优先级低于系统环境变量
DEFAULT_ENV_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
if os.path.exists(DEFAULT_ENV_PATH):
    load_dotenv(DEFAULT_ENV_PATH)


class Config:
    """
    轻量配置容器：读取常用的环境变量并提供属性访问。
    - BASE_URL: API 服务根地址
    - TIMEOUT: HTTP 超时时间（秒）
    - RETRY: 默认重试次数

    设计上尽量与原先使用 pydantic 的接口保持一致（保留属性名），
    以便现有代码（如 pytest fixture）无需修改。
    """

    def __init__(self):
        self.BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')
        # 尝试转换为 int，失败则使用默认
        try:
            self.TIMEOUT = int(os.environ.get('TIMEOUT', '10'))
        except ValueError:
            self.TIMEOUT = 10
        try:
            self.RETRY = int(os.environ.get('RETRY', '2'))
        except ValueError:
            self.RETRY = 2


def load_config():
    """
    创建并返回 Config 实例。保持与原先 load_config() 的调用签名一致。
    """
    return Config()
