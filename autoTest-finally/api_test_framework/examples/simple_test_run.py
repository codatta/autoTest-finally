# examples/simple_test_run.py
# 简单示例：展示如何直接使用 APIClient 发起请求（用于快速手工验证）。

from api_test_framework.core.http_client import APIClient


if __name__ == '__main__':
    # 这里直接使用 jsonplaceholder 的公共测试服务作为示例
    c = APIClient(base_url='https://jsonplaceholder.typicode.com')
    resp = c.get('/')
    print('status', resp.status_code)
