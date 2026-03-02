# core/logger.py
# 全局日志工厂：为模块提供统一格式和 StreamHandler，避免重复添加 handler 导致重复日志。

import logging


def get_logger(name: str = 'api_test_framework'):
    """
    获取一个配置好的 logger 实例。
    - 如果 logger 已经配置过 handler，则直接返回，避免多次添加 handler 导致日志重复。
    - 默认为 INFO 级别，输出到标准输出（StreamHandler）。

    用法：
        logger = get_logger(__name__)
        logger.info('message')
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
