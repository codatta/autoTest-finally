# api/order_api.py
# 订单模块占位示例：封装订单相关接口（示例方法，具体实现按业务调整）。

from api_test_framework.api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    """订单 API 示例：提供获取订单的接口封装。"""

    def get_order(self, order_id):
        """根据订单 ID 获取订单信息，返回 requests.Response。"""
        return self.get(f"/orders/{order_id}")
