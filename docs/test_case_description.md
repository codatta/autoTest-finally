# 测试模块功能说明

## 测试目录结构

```
tests/
├── api/                    # 单个接口测试
│   ├── test_login.py       # 登录认证接口
│   ├── test_user.py        # 用户接口
│   ├── test_checkin.py     # 签到接口
│   ├── test_quest.py       # 任务接口
│   └── test_frontier.py    # Frontier接口
└── scenario/               # 场景测试
    ├── test_login_flow.py         # 登录流程场景
    ├── test_checkin_flow.py       # 签到流程场景
    └── test_submission_flow.py    # 任务提交流景
```

---

## 单个接口测试 (tests/api/)

### 1. test_login.py - 登录认证模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_login_flow | 登录流程 | 私钥登录 → 获取Token → 验证用户信息 |
| test_nonce_api | Nonce接口 | 获取登录随机数 |
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

### 4. test_quest.py - 任务分类模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_get_task_categories | 获取任务分类 | 查询所有任务分类列表 |

### 5. test_frontier.py - 任务提交模块

| 用例 | 功能 | 说明 |
|------|------|------|
| test_frontier_list | 获取Frontier列表 | 查询所有项目列表 |
| test_frontier_list_with_channel | 获取指定Channel列表 | 按Channel筛选项目 |

---

## 场景测试 (tests/scenario/)

### 1. test_login_flow.py - 登录流程场景

| 用例 | 功能 | 说明 |
|------|------|------|
| test_complete_login_flow | 完整登录流程 | 登录 → 获取token → 验证token → 调用受保护接口 |

### 2. test_checkin_flow.py - 签到流程场景

| 用例 | 功能 | 说明 |
|------|------|------|
| test_checkin_and_verify_status | 签到后验证状态 | 执行签到 → 查询签到状态 → 验证 is_check_in=true |

### 3. test_submission_flow.py - 任务提交流景

| 用例 | 功能 | 说明 |
|------|------|------|
| test_submit_task_and_verify_in_history | 提交任务验证 | 提交任务 → 查询提交历史 → 验证记录存在 |

---

## 测试执行命令

### 单个接口测试

```bash
# 运行所有单个接口测试
pytest tests/api/ -v

# 运行指定模块
pytest tests/api/test_user.py -v
```

### 场景测试

```bash
# 运行所有场景测试
pytest tests/scenario/ -v

# 运行指定场景
pytest tests/scenario/test_checkin_flow.py -v
```

### 运行所有测试

```bash
pytest tests/ -v
```

---

## 测试流程（端到端）

```
单个接口测试 (tests/api/)
    ↓
场景测试 (tests/scenario/)
    ↓
邮件报告（批量执行时）
```