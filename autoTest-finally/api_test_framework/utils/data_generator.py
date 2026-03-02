# utils/data_generator.py
# 测试用数据生成器：提供简单的随机数据生成函数，便于构造测试 payload。

import random


def fake_email():
    """生成一个简单的伪造邮箱地址，例如 user1234@example.com。"""
    return f"user{random.randint(1000,9999)}@example.com"
