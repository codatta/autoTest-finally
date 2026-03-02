# api/__init__.py
# api 包的初始化模块：对外统一导出常用客户端或接口类，方便从上层导入。

from api_test_framework.core.http_client import APIClient

__all__ = ['APIClient']
