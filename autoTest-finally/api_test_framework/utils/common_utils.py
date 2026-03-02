# utils/common_utils.py
# 常用工具函数集合（示例）：时间戳/格式化等。可按需扩展。

import time


def now_ts():
    """
    返回当前 UNIX 时间戳（整数秒）。

    用途：测试用例中生成唯一值、时间比较等场景。
    示例：
        ts = now_ts()
    """
    return int(time.time())
