我已经**直接在你现有文档里新增了「无Token / 无效Token访问接口」的统一用例**，包含：
- 模块：用户模块（最适合放这个通用鉴权用例）
- 明确返回 **401** + 你指定的错误信息
- 格式完全对齐、可直接复制进你的 MD

下面是**插入后完整、干净的 MD 文档**，你直接全选复制即可。

# 接口自动化测试用例文档
## 文档信息
- 文档版本：V1.0
- 测试类型：接口单功能测试 + 业务场景测试
- 测试框架：pytest
- 代码目录：tests/api/、tests/scenario/

---

## 1. 登录模块（单接口测试）
路径：`tests/api/test_login.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| API-LOGIN-001 | 登录流程（私钥登录获取Token） | 1. 测试环境正常；2. 持有合法私钥 | 1. 调用Nonce接口获取随机数；2. 钱包签名；3. 调用登录接口获取Token；4. 验证用户信息 | 登录成功，返回success=True，data包含有效Token和用户信息 | 1. 响应不为None；2. success=True；3. data包含token字段 | pytest tests/api/test_login.py::test_login_flow -v |
| API-LOGIN-002 | 获取登录随机数（Nonce接口） | 1. 测试环境接口可访问 | 1. 调用Nonce接口 | 返回success=True，包含有效nonce随机数 | 1. 响应不为None；2. success=True；3. 包含nonce字段 | pytest tests/api/test_login.py::test_nonce_api -v |
| API-LOGIN-003 | 钱包签名功能测试 | 1. 持有合法私钥；2. 获取有效nonce | 1. 调用钱包签名接口，传入私钥和nonce | 签名成功，返回合法签名信息 | 1. 响应不为None；2. 签名信息格式正确 | pytest tests/api/test_login.py::test_wallet_signature -v |

---

## 2. 用户模块（单接口测试）
路径：`tests/api/test_user.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| API-USER-001 | 获取用户基本信息 | 1. 用户已登录，Token有效 | 1. 调用获取用户信息接口 | 返回success=True，data包含用户ID、昵称等核心信息 | 1. 响应不为None；2. success=True；3. data包含user_id字段 | pytest tests/api/test_user.py::test_get_user_info -v |
| API-USER-002 | 获取用户详细资料 | 1. 用户已登录，Token有效 | 1. 调用获取用户资料接口 | 返回success=True，data包含用户详细资料（如头像、简介） | 1. 响应不为None；2. success=True；3. data包含profile字段 | pytest tests/api/test_user.py::test_get_profile -v |
| API-USER-003 | 获取用户余额（积分/代币） | 1. 用户已登录，Token有效 | 1. 调用获取用户余额接口 | 返回success=True，data包含用户积分/代币余额 | 1. 响应不为None；2. success=True；3. data包含balance字段 | pytest tests/api/test_user.py::test_get_balance -v |
| API-USER-004 | 获取用户钱包信息 | 1. 用户已登录，Token有效 | 1. 调用获取钱包信息接口 | 返回success=True，包含钱包地址、连接状态 | 1. 响应不为None；2. success=True；3. 包含wallet_address字段 | pytest tests/api/test_user.py::test_get_wallet_info -v |
| API-USER-005 | Token有效性验证 | 1. 已获取登录Token | 1. 调用Token验证接口，传入Token | 返回success=True，验证Token有效 | 1. 响应不为None；2. success=True；3. 提示Token有效 | pytest tests/api/test_user.py::test_token_exists -v |
| API-USER-006 | 无Token访问需要登录的接口 | 1. 测试环境正常；2. 未登录、无Token | 1. 调用需要登录的用户信息接口；2. 不携带任何Token | 返回401，错误信息：{"errorMessage": "The JWT token is invalid. Please verify that the token is correct."} | 1. 响应状态码=401；2. 返回指定errorMessage；3. 未返回用户数据 | pytest tests/api/test_user.py::test_access_without_token -v |

---

## 3. 签到模块（单接口测试）
路径：`tests/api/test_checkin.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| API-CHECKIN-001 | 查询当日签到状态 | 1. 用户已登录，Token有效 | 1. 调用查询签到状态接口 | 返回success=True，包含当日是否已签到、累计签到天数 | 1. 响应不为None；2. success=True；3. 包含is_check_in、total_days字段 | pytest tests/api/test_checkin.py::test_consult_today_checkin_status -v |

---

## 4. 任务模块（单接口测试）
路径：`tests/api/test_quest.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| API-QUEST-001 | 获取所有任务分类 | 1. 测试环境接口可访问 | 1. 调用获取任务分类接口 | 返回success=True，data包含所有任务分类列表 | 1. 响应不为None；2. success=True；3. data为列表格式 | pytest tests/api/test_quest.py::test_get_task_categories -v |

---

## 5. Frontier模块（单接口测试）
路径：`tests/api/test_frontier.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| API-FRONTIER-001 | 获取Frontier项目列表 | 1. 测试环境接口可访问 | 1. 调用获取Frontier列表接口 | 返回success=True，data包含所有Frontier项目列表 | 1. 响应不为None；2. success=True；3. data为列表格式 | pytest tests/api/test_frontier.py::test_frontier_list -v |
| API-FRONTIER-002 | 获取指定Channel的Frontier列表 | 1. 测试环境接口可访问；2. 持有合法Channel ID | 1. 调用接口，传入Channel ID筛选 | 返回success=True，data包含该Channel下的所有项目 | 1. 响应不为None；2. success=True；3. 列表中项目属于目标Channel | pytest tests/api/test_frontier.py::test_frontier_list_with_channel -v |

---

## 6. 场景测试用例

### 6.1 登录场景测试
路径：`tests/scenario/test_login_flow.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| SCEN-LOGIN-001 | 完整登录流程（正常场景） | 1. 测试环境正常；2. 持有合法私钥 | 1. 获取nonce；2. 钱包签名；3. 登录获取Token；4. 验证Token；5. 调用受保护接口 | 完整流程无异常，登录成功，受保护接口可正常访问 | 1. 登录接口success=True；2. Token验证有效；3. 受保护接口调用成功 | pytest tests/scenario/test_login_flow.py::test_complete_login_flow -v |
| SCEN-LOGIN-002 | 登录流程（异常场景-非法私钥） | 1. 测试环境正常；2. 持有非法私钥 | 1. 获取nonce；2. 用非法私钥签名；3. 调用登录接口 | 登录失败，返回success=False，提示私钥非法 | 1. 登录接口success=False；2. 错误信息包含“私钥非法”；3. 未返回Token | pytest tests/scenario/test_login_flow.py::test_login_with_invalid_private_key -v |
| SCEN-LOGIN-003 | 登录流程（边界场景-过期nonce） | 1. 测试环境正常；2. 持有合法私钥；3. 获取过期nonce | 1. 使用过期nonce签名；2. 调用登录接口 | 登录失败，返回success=False，提示nonce过期 | 1. 登录接口success=False；2. 错误信息包含“nonce过期”；3. 未返回Token | pytest tests/scenario/test_login_flow.py::test_login_with_expired_nonce -v |

---

### 6.2 签到场景测试
路径：`tests/scenario/test_checkin_flow.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| SCEN-CHECKIN-001 | 签到流程（正常场景-未签到） | 1. 用户已登录；2. 当日未签到 | 1. 执行签到接口；2. 调用查询签到状态接口 | 签到成功，查询结果显示is_check_in=true | 1. 签到接口success=True；2. 查询接口success=True；3. is_check_in=true | pytest tests/scenario/test_checkin_flow.py::test_checkin_and_verify_status -v |
| SCEN-CHECKIN-002 | 签到流程（异常场景-重复签到） | 1. 用户已登录；2. 当日已签到 | 1. 再次执行签到接口；2. 调用查询签到状态接口 | 签到失败，提示“今日已签到”，查询状态仍为is_check_in=true | 1. 签到接口success=False；2. 错误信息包含“今日已签到”；3. 查询接口is_check_in=true | pytest tests/scenario/test_checkin_flow.py::test_checkin_duplicate -v |
| SCEN-CHECKIN-003 | 签到流程（异常场景-Token失效） | 1. 用户已登录但Token失效；2. 当日未签到 | 1. 执行签到接口 | 签到失败，返回success=False，提示Token失效 | 1. 签到接口success=False；2. 错误信息包含“Token失效”；3. 未完成签到 | pytest tests/scenario/test_checkin_flow.py::test_checkin_with_invalid_token -v |

---

### 6.3 任务提交场景测试
路径：`tests/scenario/test_submission_flow.py`

| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| SCEN-SUBMIT-001 | 任务提交（正常场景-合法数据） | 1. 用户已登录，Token有效；2. 测试任务数据（task_id/frontier_id）已准备 | 1. 调用提交任务接口；2. 调用提交历史查询接口；3. 验证记录存在 | 提交成功，历史列表中包含本次提交的task_id | 1. 提交接口success=True；2. 历史查询success=True；3. 找到目标task_id | pytest tests/scenario/test_submission_flow.py::test_submit_task_and_verify_in_history -v |
| SCEN-SUBMIT-002 | 任务提交（异常场景-无效task_id） | 1. 用户已登录，Token有效；2. 准备无效task_id | 1. 调用提交任务接口，传入无效task_id；2. 查看接口返回 | 提交失败，返回success=False，提示task_id无效 | 1. 提交接口success=False；2. 错误信息包含“task_id无效”；3. 历史记录无该提交 | pytest tests/scenario/test_submission_flow.py::test_submit_with_invalid_task_id -v |
| SCEN-SUBMIT-003 | 任务提交（异常场景-重复提交） | 1. 用户已登录，Token有效；2. 已提交过该task_id | 1. 再次调用提交任务接口；2. 调用历史查询接口验证 | 提交失败，提示“重复提交”，历史记录仅存在1条该task_id记录 | 1. 提交接口success=False；2. 错误信息包含“重复提交”；3. 历史记录无新增 | pytest tests/scenario/test_submission_flow.py::test_submit_duplicate_task -v |

---

## 7. 用例模板

### 7.1 单接口用例模板
| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| API-模块-序号 | 接口功能描述 | 1. xxx；2. xxx | 1. 调用xxx接口；2. （可选）传入参数 | 返回success=True，包含xxx数据 | 1. 响应不为None；2. success=True；3. 包含xxx字段 | pytest tests/api/xxx.py::test_xxx -v |

### 7.2 场景用例模板
| 用例编号 | 用例名称 | 前置条件 | 步骤 | 预期结果 | 断言点 | 测试命令 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| SCEN-场景-序号 | 流程描述 | 1. xxx；2. xxx | 1. 执行xxx步骤；2. 执行xxx步骤；3. 验证结果 | 流程无异常，达到预期业务效果 | 1. 各接口success=True；2. 业务数据符合预期 | pytest tests/scenario/xxx.py::test_xxx -v |

---

## 我新增的这条用例说明（你可直接使用）
**用例编号**：API-USER-006
**用例名称**：无Token访问需要登录的接口
**预期结果**：固定返回你给的 401 错误信息
**断言点**：状态码401 + 错误信息完全匹配

如果你需要，我还能帮你把**签到、任务、Frontier 也各加一条无Token用例**。