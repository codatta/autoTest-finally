# testcases/full/test_web3_login.py
# Web3 钱包登录的示例测试：流程为请求 nonce -> 对 message 签名 -> 提交登录 -> 验证 token

import os
import pytest
from api_test_framework.core.http_client import APIClient
from api_test_framework.utils.web3_utils import address_from_private_key, sign_message_hex
from eth_account import Account

# 方便测试，从环境变量读取私钥；如果没有，使用占位（请在实际运行前替换为测试私钥）
TEST_PRIVATE_KEY = os.environ.get('TEST_PRIVATE_KEY', '0x' + '1' * 64)
# 可选：从环境读取 cookie（例如 curl 中的 _c_WBKFRo），不应写入代码库
TEST_COOKIE = os.environ.get('TEST_COOKIE', '')


@pytest.mark.full
def test_web3_wallet_login_flow():
    # 从配置或环境中读取 base_url；这里尝试从环境变量/默认值获取
    base_url = os.environ.get('BASE_URL', 'https://app-test.b18a.io')
    client = APIClient(base_url=base_url)

    # 如果提供了 cookie，则注入到 session（仅用于测试）
    if TEST_COOKIE:
        # 解析 cookie 字符串（例如 "_c_WBKFRo=evRht..." 形式），
        # 尝试简单解析为 key=value
        try:
            k, v = TEST_COOKIE.split('=', 1)
            client.session.cookies.set(k.strip(), v.strip())
        except Exception:
            # 如果格式不是 key=value，直接将整个字符串作为 Cookie header
            client.session.headers.update({'Cookie': TEST_COOKIE})

    # 使用私钥推导 address
    address = address_from_private_key(TEST_PRIVATE_KEY)

    # 1) 请求 nonce/message
    # 根据你给出的 curl 示例，nonce 接口是 POST https://app-test.b18a.io/api/v2/user/nonce
    # 请求体: {"account_type":"block_chain"}
    nonce_resp = client.post('/api/v2/user/nonce', json={"account_type": "block_chain"})
    assert nonce_resp.status_code == 200
    nonce_payload = nonce_resp.json()
    # 适配实际返回：后端可能把 nonce 放在 'data' 字段中，或者返回 'nonce' / 'message'
    message_to_sign = nonce_payload.get('message') or nonce_payload.get('nonce') or nonce_payload.get('data')
    assert message_to_sign, f"nonce/message not found in response: {nonce_payload}"

    # 2) 使用私钥签名（Ethereum Signed Message）
    signature = sign_message_hex(TEST_PRIVATE_KEY, message_to_sign)

    # 3) 提交登录
    login_body = {
        "account_type": "block_chain",
        "account_enum": "C",
        "connector": "codatta_wallet",
        "inviter_code": "",
        "wallet_name": "OKX Wallet",
        "address": address,
        "chain": "56",
        # 后端实际返回的 nonce 可能在 data 字段
        "nonce": nonce_payload.get('nonce') or nonce_payload.get('data') or '',
        "signature": signature,
        "message": message_to_sign,
        "source": {"device": "WEB", "channel": "codatta-platform-website", "app": "codatta-platform-website"}
    }

    login_resp = client.post('/api/v2/user/login', json=login_body)
    assert login_resp.status_code in (200, 201)
    login_json = login_resp.json()
    # 根据后端返回字段断言 token 或 user 信息存在
    token = login_json.get('token') or (login_json.get('data') or {}).get('token')
    assert token, f"login response did not contain token: {login_json}"

    # 简单验证 token 看起来像一个 JWT（有两处 '.' 分隔），这是一个基本的格式检查而非安全验证
    assert token.count('.') == 2, f"token does not look like a JWT: {token}"
