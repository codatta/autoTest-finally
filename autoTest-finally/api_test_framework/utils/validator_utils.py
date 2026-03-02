# utils/validator_utils.py
# 测试断言辅助工具：封装常用断言，保持测试代码简洁。


def assert_status_code(resp, code=200):
    """
    断言响应的 HTTP 状态码是否等于期望值，便于在测试中复用。

    - resp: requests.Response 对象
    - code: 期望的状态码（默认 200）
    """
    assert resp.status_code == code
