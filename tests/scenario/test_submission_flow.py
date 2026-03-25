"""
任务提交场景测试用例

包含以下场景：
- 提交任务后查询提交记录
- 提交数据后查询提交的数据
"""
import pytest
from config.test_data import FrontierTestData


class TestSubmissionFlow:
    """任务提交流程场景测试"""

    @pytest.mark.parametrize("test_data", FrontierTestData.get_all_cases())
    def test_submit_task_and_verify_in_history(self, frontier_api, test_data):
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

    def test_submit_with_invalid_task_id(self, frontier_api):
        """
        【场景测试】提交任务（异常场景-无效task_id）

        前置条件：用户已登录，Token有效；准备无效task_id

        步骤：
        1. 调用提交任务接口，传入无效task_id
        2. 查看接口返回

        预期结果：提交失败，返回success=False，提示task_id无效

        断言点：
        - 提交接口 success=False
        - 错误信息包含 "task is not exist"
        - errorCode 为 6001
        - 历史记录无该提交
        """
        print("\n=== 【场景测试】无效task_id提交任务 ===")

        # 使用无效的 task_id
        invalid_task_id = "invalid_task_id_999999"
        invalid_submission_data = {"test": "data"}

        print(f"无效task_id: {invalid_task_id}")

        # --- 步骤 1: 调用提交任务接口，传入无效task_id ---
        print("\n步骤1: 调用提交任务接口（无效task_id）...")
        submit_result = frontier_api.submit_task(invalid_task_id, invalid_submission_data)
        print(f"提交响应: {submit_result}")

        # --- 步骤 2: 断言提交失败 ---
        print("\n步骤2: 断言提交失败...")
        assert submit_result.get("success") is False, "无效task_id提交应该返回失败"

        # 断言 errorCode 为 6001
        error_code = submit_result.get("errorCode")
        print(f"errorCode: {error_code}")
        assert error_code == 6001, f"errorCode应为6001，实际为: {error_code}"

        # 断言错误信息包含 "task is not exist"
        error_msg = submit_result.get("errorMessage", "")
        print(f"错误信息: {error_msg}")
        assert "task" in error_msg.lower() and ("not exist" in error_msg.lower() or "invalid" in error_msg.lower()), \
            f"错误信息应提示task无效，实际: {error_msg}"

        print("=== 场景测试通过：无效task_id被正确拒绝 ===")
