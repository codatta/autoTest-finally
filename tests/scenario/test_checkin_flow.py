"""
签到场景测试用例

包含以下场景：
- 正常签到流程：签到 → 验证签到状态
- 异常场景：重复签到
"""
import pytest


class TestCheckInFlow:
    """签到流程场景测试"""

    def test_checkin_and_verify_status(self, checkin_api):
        """
        【场景测试】签到 → 验证签到状态（正常场景-未签到）

        前置条件：用户已登录，当日未签到

        步骤：
        1. 先调用查询签到状态接口，确认当日未签到
        2. 执行签到接口
        3. 再次调用查询签到状态接口
        4. 断言签到后 is_check_in=true

        预期结果：签到成功，查询结果显示 is_check_in=true

        断言点：
        - 步骤1查询：is_check_in=false（确认未签到）
        - 签到接口 success=True
        - 步骤3查询：is_check_in=true
        """
        print("\n=== 【场景测试】签到 → 验证签到状态 ===")

        # --- 步骤 1: 先查询签到状态，确认当日未签到 ---
        print("\n步骤1: 查询签到状态（确认未签到）...")
        consult_result = checkin_api.consult()
        print(f"查询响应: {consult_result}")

        if consult_result.get("errorCode") == 404:
            print("接口路径不存在，跳过")
            pytest.skip("接口不存在，跳过测试")

        data = consult_result.get("data", {})
        is_check_in_before = data.get("is_check_in")
        print(f"签到前状态: is_check_in = {is_check_in_before}")

        # 如果已签到，跳过测试（避免重复签到）
        if is_check_in_before is True:
            print("[INFO] 今日已签到，跳过测试")
            pytest.skip("今日已签到，无法测试签到流程")

        # --- 步骤 2: 执行签到接口 ---
        print("\n步骤2: 执行签到接口...")
        checkin_result = checkin_api.check_in()
        print(f"签到响应: {checkin_result}")

        # 断言签到成功
        assert checkin_result.get("success") is True, f"签到失败: {checkin_result}"

        # --- 步骤 3: 再次查询签到状态 ---
        print("\n步骤3: 查询签到状态（验证签到结果）...")
        consult_result = checkin_api.consult()
        print(f"查询响应: {consult_result}")

        # --- 步骤 4: 断言签到状态为 true ---
        print("\n步骤4: 断言签到状态...")
        assert consult_result is not None, "响应不能为空"
        assert consult_result.get("success") is True, f"查询签到状态失败: {consult_result}"
        assert "data" in consult_result, "响应缺少data字段"

        data = consult_result.get("data", {})
        is_check_in_after = data.get("is_check_in")

        print(f"签到后状态: is_check_in = {is_check_in_after}")

        # 核心断言：签到后 is_check_in 应该为 true
        assert is_check_in_after is True, (
            f"签到后 is_check_in 应为 true，实际为 {is_check_in_after}。"
            f"完整响应: {consult_result}"
        )

        print("=== 场景测试通过：签到后签到状态为 true ===")

    def test_checkin_duplicate(self, checkin_api):
        """
        【场景测试】重复签到（异常场景-重复签到）

        前置条件：用户已登录，当日已签到

        步骤：
        1. 先调用查询签到状态接口，确认当日已签到
        2. 再次执行签到接口
        3. 调用查询签到状态接口验证

        预期结果：签到失败，提示"今日已签到"，查询状态仍为 is_check_in=true

        断言点：
        - 重复签到接口 success=False
        - 错误信息包含"already"或类似提示
        - 查询接口 is_check_in=true
        """
        print("\n=== 【场景测试】重复签到 ===")

        # --- 步骤 1: 先查询签到状态，确认当日已签到 ---
        print("\n步骤1: 查询签到状态...")
        consult_result = checkin_api.consult()
        print(f"查询响应: {consult_result}")

        if consult_result.get("errorCode") == 404:
            print("接口路径不存在，跳过")
            pytest.skip("接口不存在，跳过测试")

        data = consult_result.get("data", {})
        is_check_in = data.get("is_check_in")

        # 如果今日未签到，先执行签到
        if is_check_in is not True:
            print("\n当日未签到，先执行签到...")
            checkin_api.check_in()
            # 再次查询确认
            consult_result = checkin_api.consult()
            data = consult_result.get("data", {})
            is_check_in = data.get("is_check_in")

        print(f"当前签到状态: is_check_in = {is_check_in}")

        # 确认当日已签到
        assert is_check_in is True, "需要先完成签到才能测试重复签到"

        # --- 步骤 2: 再次执行签到接口 ---
        print("\n步骤2: 再次执行签到接口...")
        checkin_result = checkin_api.check_in()
        print(f"签到响应: {checkin_result}")

        # --- 步骤 3: 断言重复签到失败 ---
        print("\n步骤3: 断言重复签到失败...")
        assert checkin_result.get("success") is False, "重复签到应该返回失败"

        error_msg = checkin_result.get("errorMessage", "")
        print(f"错误信息: {error_msg}")

        # 断言错误信息包含"already"或"repeat"等提示
        assert "already" in error_msg.lower() or "repeat" in error_msg.lower() or \
               "checked" in error_msg.lower() or "today" in error_msg.lower(), \
            f"错误信息应该提示今日已签到，实际: {error_msg}"

        # --- 步骤 4: 查询签到状态验证仍为已签到 ---
        print("\n步骤4: 查询签到状态验证...")
        consult_result = checkin_api.consult()
        data = consult_result.get("data", {})
        is_check_in = data.get("is_check_in")

        print(f"is_check_in = {is_check_in}")
        assert is_check_in is True, "重复签到后签到状态仍应为 true"

        print("=== 场景测试通过：重复签到被正确拒绝 ===")
