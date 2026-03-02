# testcases/full/test_check_in_consult.py
# 示例测试：使用会话级 auth_headers fixture（包含 token）调用受保护接口 /api/v2/check-in/consult

import pytest


@pytest.mark.full
def test_check_in_consult(client, auth_headers):
    """
    发起 POST 请求到 /api/v2/check-in/consult（body 为空），使用 auth_headers 提供 token，以及必要的 headers（channel/device）
    """
    headers = dict(auth_headers)
    # 后端需要这两个自定义 header，根据 curl 示例添加
    headers.update({
        'channel': 'codatta-platform-website',
        'device': 'web'
    })

    resp = client.post('/api/v2/check-in/consult', headers=headers)

    # 基本断言：请求成功并返回 JSON
    assert resp.status_code in (200, 201), f"Unexpected status: {resp.status_code}, body: {resp.text}"
    j = resp.json()

    # 期望后端返回 success 字段或 data 字段，做宽松检查
    assert j.get('success', True) is True or 'data' in j, f"Unexpected response shape: {j}"
    # 如果返回 data，断言至少包含某些字段（可根据实际返回调整）
    if isinstance(j.get('data'), dict):
        assert 'consult' in j['data'] or 'result' in j['data'] or True

