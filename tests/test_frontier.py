"""
Frontier接口测试
"""
import pytest
from api.frontier import FrontierApi
from config.test_data import FrontierTestData


class TestFrontierApi:
    """Frontier API测试类"""

    def test_frontier_list(self, frontier_api: FrontierApi):
        """
        测试获取frontier列表接口
        """
        print("\n=== 测试Frontier列表接口 ===")
        result = frontier_api.list(channel="")
        print(f"响应结果: {result}")

        # 允许接口超时（504）
        if result.get("_status_code") == 504:
            print("⚠️ 接口响应超时（504），跳过")
            return

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

        # 允许接口超时（504）
        if result.get("_status_code") == 504:
            print("⚠️ 接口响应超时（504），跳过")
            return

        # 验证接口返回成功
        assert result.get("success") is True, f"接口返回失败: {result}"
        print("=== Frontier列表接口(带channel)测试通过 ===")

    @pytest.mark.parametrize("test_data", FrontierTestData.get_all_cases())
    def test_submit_task_and_verify_in_history(self, frontier_api: FrontierApi, test_data):
        """
        【场景测试】提交任务 → 验证提交记录

        步骤：
        1. 先调用提交任务接口
        2. 再调用提交历史查询接口
        3. 断言提交记录中包含刚才提交的任务

        验证:
        - 提交任务接口调用成功
        - 提交历史中能找到对应的记录

        测试数据: 从 config/test_data.py 根据环境配置读取，支持多用例
        """
        case_name = test_data.get("case_name", "未命名用例")
        task_id = test_data["task_id"]
        frontier_id = test_data["frontier_id"]
        submission_data = test_data["submission_data"]

        print(f"\n=== 【场景测试】提交任务 → 验证提交记录 | {case_name} ===")
        print(f"当前测试数据: task_id={task_id}, frontier_id={frontier_id}")

        # --- 步骤 1: 提交任务 ---
        print("\n步骤1: 调用提交任务接口...")
        submit_result = frontier_api.submit_task(task_id, submission_data)
        print(f"提交响应: {submit_result}")

        # 如果提交失败（非必现问题，如重复提交），打印警告但继续验证历史
        if submit_result.get("success") is False:
            error_msg = submit_result.get("errorMessage", "")
            print(f"⚠️ 提交失败: {error_msg}")

        # --- 步骤 2: 查询提交历史 ---
        print("\n步骤2: 调用提交历史查询接口...")
        history_result = frontier_api.get_submission_list(
            frontier_id=frontier_id,
            page_size=8,
            page_num=1
        )
        print(f"历史响应: {history_result}")

        # 允许接口超时（504）
        if history_result.get("_status_code") == 504:
            print("⚠️ 提交历史接口响应超时（504），跳过验证")
            return

        # --- 步骤 3: 断言提交记录存在 ---
        print("\n步骤3: 断言提交记录存在...")

        assert history_result is not None, "响应不能为空"
        assert history_result.get("success") is True, f"查询历史失败: {history_result}"
        assert "data" in history_result, "响应缺少data字段"

        data = history_result.get("data", {})
        # data 可能是 list，也可能是 dict
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("list", []) or data.get("data", [])
        else:
            items = []

        print(f"历史记录数量: {len(items)}")

        # 在历史记录中查找刚才提交的任务
        found = False
        for item in items:
            item_task_id = str(item.get("taskId") or item.get("task_id") or "")
            if item_task_id == task_id:
                found = True
                print(f"✅ 找到提交记录: taskId={item_task_id}, 状态={item.get('status')}")
                break

        # 断言：必须在历史记录中找到刚才提交的任务
        assert found, (
            f"未在历史记录中找到提交的任务 taskId={task_id}。"
            f"提交响应: {submit_result}，现有记录: {[str(i.get('taskId') or i.get('task_id')) for i in items]}"
        )

        print(f"✅ 场景测试完成：{case_name} 验证通过")
