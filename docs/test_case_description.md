# 测试模块功能说明

## 模块清单

| 序号 | 测试文件 | 功能模块 | 说明 |
|------|----------|----------|------|
| 1 | test_login.py | 登录认证 | 测试登录流程、Nonce、钱包签名 |
| 2 | test_user.py | 用户信息 | 测试获取用户信息、资料、余额、钱包 |
| 3 | test_checkin.py | 签到 | 测试签到功能、签到状态查询 |
| 4 | test_quest.py | 任务分类 | 测试获取任务分类列表 |
| 5 | test_frontier.py | 任务提交 | 测试提交Task、查询提交历史 |

---

## 详细说明

### 1. test_login.py - 登录认证模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_login_flow | 登录流程 | 私钥登录 → 获取Token → 验证用户信息 |
| test_nonce_api |Nonce接口 | 获取登录随机数 |
| test_wallet_signature | 钱包签名 | 测试区块链签名功能 |

### 2. test_user.py - 用户信息模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_get_user_info | 获取用户信息 | 查询当前用户基本信息 |
| test_get_profile | 获取用户资料 | 查询用户详细资料 |
| test_get_balance | 获取用户余额 | 查询用户积分/代币余额 |
| test_get_wallet_info | 获取钱包信息 | 查询钱包地址、连接状态 |
| test_token_exists | Token验证 | 验证登录Token有效性 |

### 3. test_checkin.py - 签到模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_consult_today_checkin_status | 查询签到状态 | 查询当天是否已签到、累计签到天数 |
| test_checkin_and_verify_status | 签到验证 | 执行签到 → 验证签到状态变为已签到 |

### 4. test_quest.py - 任务分类模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_get_task_categories | 获取任务分类 | 查询所有任务分类列表 |

### 5. test_frontier.py - 任务提交模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_frontier_list | 获取Frontier列表 | 查询所有项目列表 |
| test_frontier_list_with_channel | 获取指定Channel列表 | 按Channel筛选项目 |
| test_submit_task_and_verify_in_history | 提交Task验证 | 提交任务 → 查询历史 → 验证记录存在 |

---

## 测试流程（端到端）

```
登录模块 (test_login)
    ↓
用户模块 (test_user)
    ↓
签到模块 (test_checkin)
    ↓
任务分类模块 (test_quest)
    ↓
任务提交模块 (test_frontier)
```