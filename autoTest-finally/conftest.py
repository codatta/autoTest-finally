"""
Pytest配置文件
提供全局fixture和配置
"""
import pytest
import os
from datetime import datetime
from core.auth import Auth
from core.http_client import HttpClient
from api.user import UserApi
from api.frontier import FrontierApi
from config.settings import config


# 设置环境变量（如果没有设置的话）
def pytest_configure(config):
    """pytest启动时的配置"""
    # 从环境变量读取私钥，如果没有则使用用户提供的私钥
    if not os.getenv("PRIVATE_KEY"):
        os.environ["PRIVATE_KEY"] = "0x40e68d7c277fbbd3399e7568011ec02cdb5f1009c1db15d883ef51bb41deb028"

    # 设置BASE_URL环境变量
    if not os.getenv("BASE_URL"):
        os.environ["BASE_URL"] = "https://app-test.b18a.io"


def pytest_load_initial_conftests(early_config, parser, args):
    """最早加载的conftest，设置报告路径"""
    # 创建报告目录
    report_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(report_dir, exist_ok=True)

    # 生成带时间戳的报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.html"
    report_path = os.path.join(report_dir, report_filename)

    # 动态添加 --html 参数到命令行
    if "--html" not in args:
        args.append("--html")
        args.append(report_path)

    # 设置 self-contained-html
    if "--self-contained-html" not in args:
        args.append("--self-contained-html")


@pytest.fixture(scope="session")
def private_key():
    """获取私钥"""
    return os.getenv("PRIVATE_KEY")


@pytest.fixture(scope="session")
def auth(private_key):
    """
    创建认证实例（session级别，整个测试会话只登录一次）
    """
    print(f"\n=== 初始化认证，登录获取token ===")
    auth_instance = Auth(private_key=private_key)
    token = auth_instance.login()
    print(f"=== 登录成功，token: {token[:50]}... ===")
    return auth_instance


@pytest.fixture(scope="session")
def token(auth):
    """
    获取token（session级别）
    """
    return auth.get_token()


@pytest.fixture(scope="session")
def client(auth):
    """
    获取已认证的HTTP客户端（session级别）
    """
    return auth.get_client()


@pytest.fixture(scope="session")
def user_api(client):
    """
    获取用户API实例
    """
    return UserApi(client)


@pytest.fixture(scope="session")
def frontier_api(client):
    """
    获取Frontier API实例
    """
    return FrontierApi(client)


@pytest.fixture
def fresh_client(auth):
    """
    获取新的HTTP客户端（function级别，每次测试都新建）
    """
    return auth.get_client()


@pytest.fixture
def fresh_user_api(auth):
    """
    获取新的用户API实例（function级别）
    """
    client = auth.get_client()
    return UserApi(client)
