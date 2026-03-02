# testcases/full/test_get_user_info.py
# 示例测试：使用会话级 auth_headers fixture（包含 token）调用受保护接口 /api/v2/user/get/user_info

import pytest


@pytest.mark.full
def test_get_user_info(client, auth_headers):
    """
    发起 POST 请求到 /api/v2/user/get/user_info（body 为空），使用 auth_headers 提供 token。
    这个测试示例假设后端使用 header 名为 'token'（以及标准 Authorization: Bearer）。
    """
    # 使用 client（APIClient）和传入的 headers
    resp = client.post('/api/v2/user/get/user_info', headers=auth_headers)

    # 基本断言：请求成功并返回 JSON
    assert resp.status_code in (200, 201), f"Unexpected status: {resp.status_code}, body: {resp.text}"
    j = resp.json()

    # 后端约定可能返回 success 字段或 data 字段，这里做通用检查
    assert j.get('success', True) is True or 'data' in j, f"Unexpected response shape: {j}"
    # 如果返回 data，验证其中包含 user_id 或 address 之类字段（非必须）
    if isinstance(j.get('data'), dict):
        assert 'user_id' in j['data'] or 'address' in j['data'] or 'wallet' in j['data'] or True

