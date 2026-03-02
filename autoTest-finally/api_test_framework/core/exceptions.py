# core/exceptions.py
# 定义框架内常用的自定义异常，便于统一捕获与处理。


class APIError(Exception):
    """通用 API 错误：可用于包装请求失败、响应解析错误等场景。"""
    pass
