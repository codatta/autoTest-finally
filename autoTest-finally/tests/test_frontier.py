"""
Frontier接口测试
"""
import pytest
from api.frontier import FrontierApi


class TestFrontierApi:
    """Frontier API测试类"""

    def test_frontier_list(self, frontier_api: FrontierApi):
        """
        测试获取frontier列表接口
        """
        print("\n=== 测试Frontier列表接口 ===")
        result = frontier_api.list(channel="")
        print(f"响应结果: {result}")

        # 验证接口返回成功
        assert result.get("success") is True, f"接口返回失败: {result}"
        print("=== Frontier列表接口测试通过 ===")

    def test_frontier_list_with_channel(self, frontier_api: FrontierApi):
        """
        测试带channel参数的frontier列表接口
        """
        print("\n=== 测试Frontier列表接口(带channel) ===")
        result = frontier_api.list(channel="codatta-platform-website")
        print(f"响应结果: {result}")

        # 验证接口返回成功
        assert result.get("success") is True, f"接口返回失败: {result}"
        print("=== Frontier列表接口(带channel)测试通过 ===")
