# testcases/smoke/test_smoke_order.py
# 冒烟测试示例：快速检查获取用户接口是否可用（示例使用 jsonplaceholder）

import pytest
from api_test_framework.api.user_api import UserAPI


@pytest.mark.smoke
def test_get_user(client):
    """调用 /users/1 并断言返回 200 且包含 id 字段为 1。"""
    api = UserAPI(base_url=client.base_url, client=client)
    resp = api.get_user(1)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get('id') == 1
