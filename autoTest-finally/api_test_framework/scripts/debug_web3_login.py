# scripts/debug_web3_login.py
# 临时脚本：执行 nonce -> 签名 -> login 流程并打印每步响应，便于调试测试用例

import os
import json
from api_test_framework.core.http_client import APIClient
from api_test_framework.utils.web3_utils import address_from_private_key, sign_message_hex

TEST_PRIVATE_KEY = os.environ.get('TEST_PRIVATE_KEY', '0x' + '1' * 64)
TEST_COOKIE = os.environ.get('TEST_COOKIE', '')
BASE_URL = os.environ.get('BASE_URL', 'https://app-test.b18a.io')
# 是否在请求 API 前预热页面以获取会话 cookie/CSRF，默认启用（设置 PREHEAT_PAGE=0 可关闭）
PREHEAT_PAGE = os.environ.get('PREHEAT_PAGE', '1')

client = APIClient(base_url=BASE_URL)

# 如果用户提供了完整 cookie 字符串，优先注入到 session
if TEST_COOKIE:
    try:
        k, v = TEST_COOKIE.split('=', 1)
        client.session.cookies.set(k.strip(), v.strip())
    except Exception:
        client.session.headers.update({'Cookie': TEST_COOKIE})

# 预热页面：先 GET /account/signin 以便获取服务器下发的 Set-Cookie 或其他头（仅当 PREHEAT_PAGE 为真时）
try:
    if str(PREHEAT_PAGE).lower() in ('1', 'true', 'yes', 'y'):
        print('\nPREHEAT: GET /account/signin')
        pre_resp = client.get('/account/signin')
        print('preheat status', pre_resp.status_code)
        # 打印部分 headers 以便调试（不要打印敏感 cookie 值到日志）
        sc = pre_resp.headers.get('Set-Cookie')
        if sc:
            print('Set-Cookie header present (length):', len(sc))
        else:
            print('Set-Cookie header not present')
except Exception as e:
    # 预热失败不阻塞后续流程，但打印异常以便定位问题
    print('PREHEAT failed:', e)

address = address_from_private_key(TEST_PRIVATE_KEY)
print('address', address)

print('\nREQUEST nonce')
nonce_resp = client.post('/api/v2/user/nonce', json={"account_type": "block_chain"})
print('status', nonce_resp.status_code)
try:
    nonce_json = nonce_resp.json()
    print('json:', json.dumps(nonce_json, ensure_ascii=False, indent=2))
except Exception as e:
    print('failed to parse nonce json', e, nonce_resp.text)
    raise

message_to_sign = nonce_json.get('message') or nonce_json.get('nonce') or nonce_json.get('data')
print('message_to_sign:', message_to_sign)
signature = sign_message_hex(TEST_PRIVATE_KEY, message_to_sign)
print('signature:', signature)

login_body = {
    "account_type": "block_chain",
    "account_enum": "C",
    "connector": "codatta_wallet",
    "inviter_code": "",
    "wallet_name": "OKX Wallet",
    "address": address,
    "chain": "56",
    "nonce": nonce_json.get('nonce') or nonce_json.get('data') or '',
    "signature": signature,
    "message": message_to_sign,
    "source": {"device": "WEB", "channel": "codatta-platform-website", "app": "codatta-platform-website"}
}

print('\nREQUEST login')
login_resp = client.post('/api/v2/user/login', json=login_body)
print('status', login_resp.status_code)
try:
    login_json = login_resp.json()
    print('json:', json.dumps(login_json, ensure_ascii=False, indent=2))
except Exception as e:
    print('failed to parse login json', e, login_resp.text)
    raise

# Try extracting token
token = login_json.get('token') or (login_json.get('data') or {}).get('token') or (login_json.get('data') if isinstance(login_json.get('data'), str) else None)
print('\nEXTRACTED token:', token)

print('\nTRY protected endpoints...')
for p in ['/api/v2/user/me', '/api/v2/user', '/api/v2/user/info', '/api/v2/user/profile', '/api/v2/user/session']:
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    resp = client.get(p, headers=headers)
    print(f'GET {p} ->', resp.status_code)
    try:
        print('  json:', json.dumps(resp.json(), ensure_ascii=False))
    except Exception:
        print('  text:', resp.text[:400])

print('\nDONE')
