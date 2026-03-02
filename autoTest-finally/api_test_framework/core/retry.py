# Placeholder for retry strategies; could use tenacity or urllib3 retry
# 简单的重试工具：提供一个同步函数封装的重试逻辑，适用于短期占位与简单场景。
# 在生产环境可考虑使用 tenacity 等成熟库来实现更复杂的重试/退避策略。

from time import sleep

def simple_retry(func, retries=2, backoff=0.5, *args, **kwargs):
    """
    对给定的可调用对象进行重试。

    参数：
    - func: 可调用对象（函数或方法）
    - retries: 最大重试次数（不包含首次尝试）
    - backoff: 基础退避秒数（随重试倍增）
    - args/kwargs: 传入 func 的参数

    返回：func 的返回值，若所有尝试均失败，则抛出最后一次捕获的异常。
    """
    last = None
    for i in range(retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last = e
            # 指数退避
            sleep(backoff * (2 ** i))
    # 如果全部失败，重新抛出最后一次异常
    raise last
