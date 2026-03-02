# pytest 全局夹具：提供 config、client 等在测试中的复用实例。

import os
import tempfile
from pathlib import Path
import requests
import pytest
from api_test_framework.core.config_loader import load_config
from api_test_framework.core.http_client import APIClient
from api_test_framework.utils.web3_utils import address_from_private_key, sign_message_hex


@pytest.fixture(scope='session')
def config():
    """会话级别的配置加载：只在整个测试会话中加载一次。"""
    return load_config()


@pytest.fixture
def client(config):
    """为每个测试函数提供一个 APIClient 实例，使用从 config 中读取的 BASE_URL 与 TIMEOUT。"""
    return APIClient(base_url=config.BASE_URL, timeout=config.TIMEOUT)


def _check_base_url_reachable(base_url, timeout=5):
    """
    简要检查 base_url 是否可达：尝试向 base_url 发起 HEAD（或 GET）请求。
    返回 (True, None) 如果可达，否则 (False, error_message)。
    """
    try:
        # requests 支持传入完整 URL；选择 HEAD 更轻量；一些服务器可能不支持 HEAD，退回到 GET
        r = requests.head(base_url, timeout=timeout, allow_redirects=True)
        if r.status_code >= 400:
            # 尝试 GET 作为后备
            r = requests.get(base_url, timeout=timeout)
        # 如果请求返回且未抛异常，则认为可达
        return True, None
    except Exception as e:
        return False, str(e)


@pytest.fixture(scope='session')
def auth_token(config):
    """
    会话级夹具：提供已登录的 token 字符串。

    行为：
    - 默认每次测试会话都会执行登录流程以获取最新 token（因为 token 可能过期）。
    - 如果设置环境变量 TEST_ALWAYS_LOGIN=0，则优先使用 TEST_TOKEN（如果存在）或 TEST_TOKEN_FILE。

    优先级：
    1. 如果 TEST_ALWAYS_LOGIN==0，则尝试从环境变量 TEST_TOKEN 读取
    2. 否则或不存在时，执行自动登录流程（nonce->签名->login）以获取 token

    返回：JWT 或后端返回的 token 字符串。
    """
    # 允许通过环境变量关闭每次登录的行为（比如某些场景希望复用 token）
    always_login = os.environ.get('TEST_ALWAYS_LOGIN', '1')

    # 如果用户显式要求不每次登录且提供了 TEST_TOKEN，则直接使用
    if str(always_login) in ('0', 'false', 'no'):
        env_token = os.environ.get('TEST_TOKEN')
        if env_token:
            return env_token
        token_file = os.environ.get('TEST_TOKEN_FILE')
        if token_file and Path(token_file).exists():
            try:
                return Path(token_file).read_text().strip()
            except Exception:
                pass
        # 如果用户禁用了每次登录但未提供 token，我们仍然继续到登录流程

    # 接下来执行网络可达性检查
    base_url = os.environ.get('BASE_URL', config.BASE_URL)
    ok, err = _check_base_url_reachable(base_url)
    if not ok:
        raise RuntimeError(f'Base URL {base_url} not reachable: {err}\nPlease check network, proxy and BASE_URL env var.')

    # 使用私钥自动登录以获取 token，并缓存到临时文件（如果允许）
    private_key = os.environ.get('TEST_PRIVATE_KEY')
    if not private_key:
        raise RuntimeError('No TEST_TOKEN provided and no TEST_PRIVATE_KEY available to perform login for auth_token fixture')

    # 创建 client，并可选预热页面
    client = APIClient(base_url=base_url, timeout=config.TIMEOUT)

    # 如果提供了原始 cookie 字符串，注入到 session（例如从浏览器复制）
    test_cookie = os.environ.get('TEST_COOKIE', '')
    if test_cookie:
        try:
            k, v = test_cookie.split('=', 1)
            client.session.cookies.set(k.strip(), v.strip())
        except Exception:
            client.session.headers.update({'Cookie': test_cookie})

    # 预热页面（如果需要）
    preheat = os.environ.get('PREHEAT_PAGE', '1')
    if str(preheat).lower() in ('1', 'true', 'yes', 'y'):
        try:
            # 访问 signin 页面以让服务器下发会话 cookie（若有）
            client.get('/account/signin')
        except Exception:
            # 预热失败不阻塞登录，但打印信息
            print('Warning: preheat GET /account/signin failed, continuing to login')

    # 请求 nonce
    resp = client.post('/api/v2/user/nonce', json={"account_type": "block_chain"})
    resp.raise_for_status()
    payload = resp.json()
    message = payload.get('message') or payload.get('nonce') or payload.get('data')
    if not message:
        raise RuntimeError(f'Failed to obtain nonce/message from server: {payload}')

    # 使用私钥签名并提交登录
    addr = address_from_private_key(private_key)
    signature = sign_message_hex(private_key, message)

    login_body = {
        "account_type": "block_chain",
        "account_enum": "C",
        "connector": "codatta_wallet",
        "inviter_code": "",
        "wallet_name": "OKX Wallet",
        "address": addr,
        "chain": "56",
        "nonce": payload.get('nonce') or payload.get('data') or '',
        "signature": signature,
        "message": message,
        "source": {"device": "WEB", "channel": "codatta-platform-website", "app": "codatta-platform-website"}
    }

    login_resp = client.post('/api/v2/user/login', json=login_body)
    login_resp.raise_for_status()
    login_json = login_resp.json()

    token = login_json.get('token') or (login_json.get('data') or {}).get('token')
    if not token:
        raise RuntimeError(f'Login did not return token: {login_json}')

    # 缓存 token 到文件（如果未指定则使用临时文件并打印路径）
    out_file = os.environ.get('TEST_TOKEN_FILE')
    if not out_file:
        tf = Path(tempfile.gettempdir()) / f'api_test_token_{os.getpid()}.txt'
        out_file = str(tf)
    try:
        Path(out_file).write_text(token)
        # 仅打印调试路径，不打印 token 本身
        print(f'Cached auth token to: {out_file}')
    except Exception:
        pass

    return token


@pytest.fixture(scope='session')
def auth_headers(auth_token):
    """
    返回适用于本项目 API 的授权 headers（示例：使用 header 名为 'token'，同时提供 Authorization Bearer 形式）。
    使用时：client.get('/api/xxx', headers=auth_headers)
    """
    return {
        'token': auth_token,
        'Authorization': f'Bearer {auth_token}'
    }
