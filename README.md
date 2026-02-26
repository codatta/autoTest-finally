# api_auto_test

> 一个可扩展、分层清晰的接口自动化测试框架骨架（推荐的目录规范与使用说明）。

## 目录（快速预览）

```text
api_auto_test/                  # 项目根目录（优化后统一规范命名）
├── config/                     # 配置层：纯数据存储，无任何业务逻辑
│   ├── env/                    # 多环境配置文件目录（按环境拆分，格式统一）
│   │   ├── test.yml            # 测试环境配置（base_url、钱包私钥等）
│   │   ├── staging.yml         # 预发布环境配置
│   │   └── prod.yml            # 生产环境配置
│   └── settings.yml            # 全局通用配置（超时时间、重试次数、日志级别等）
├── core/                       # 核心抽象层：稳定不常改，定义全局规范与基础能力
│   ├── abstract/               # 抽象接口目录：定义各模块统一规范（解耦核心）
│   │   ├── http_client.py      # HTTP客户端抽象接口（规定GET/POST等方法规范）
│   │   ├── wallet.py           # Web3钱包抽象接口（规定签名、token管理规范）
│   │   ├── report.py           # 报告生成抽象接口（规定报告生成规范）
│   │   └── data_driver.py      # 数据驱动抽象接口（规定数据加载规范）
│   ├── config_manager.py       # 配置加载器：统一加载各类配置，解耦配置与业务
│   ├── exception.py            # 全局异常定义：统一异常类型，便于排查处理
│   └── logger.py               # 全局日志：统一日志格式与输出路径
├── adapters/                   # 适配器层：具体实现层，对接第三方工具/底层能力
│   ├── http/                   # HTTP客户端实现（基于抽象接口）
│   │   └── requests_client.py  # 基于requests的HTTP客户端实现（默认使用）
│   ├── wallet/                 # Web3钱包实现（基于抽象接口）
│   │   └── web3_wallet.py      # Web3钱包签名、token管理全流程实现
│   └── report/                 # 报告实现（基于抽象接口）
│       └── allure_report.py    # Allure测试报告生成实现
├── extensions/                 # 扩展层：插件化扩展，不影响核心逻辑（可灵活增减）
│   ├── data_driver/            # 数据驱动扩展（多种数据源支持）
│   ├── executor/               # 执行器扩展（多线程、异步等执行方式）
│   └── validator/              # 校验扩展（多种断言方式支持）
├── api/                        # 业务接口层：仅封装接口结构，无任何技术细节
│   ├── base_api.py             # 接口基类：封装通用请求逻辑，依赖抽象HTTP客户端
│   ├── user_api.py             # 用户模块接口封装（查询、修改等）
│   ├── order_api.py            # 订单模块接口封装（创建、查询等）
│   └── wallet_api.py           # Web3钱包相关接口封装（签名、登录等）
├── testcases/                  # 测试用例层：纯业务逻辑，仅调用接口+断言
│   ├── test_user.py            # 用户模块测试用例
│   ├── test_order.py           # 订单模块测试用例
│   ├── test_wallet.py          # Web3钱包登录相关用例
│   └── conftest.py             # pytest全局夹具：实现依赖注入，初始化测试环境
├── common/                     # 通用工具层：无业务关联，提供通用工具函数
│   └── utils.py                # 通用工具（加密、时间处理、接口重试等）
├── run_test.py                 # 统一执行入口：参数解析、执行器初始化、用例触发
└── requirements.txt            # 依赖包清单：明确版本，确保本地与CI/CD环境一致
```

---

## 说明与要点（简洁版）

下面把每一类目录用表格呈现，便于在 GitHub 上直接预览：

| 目录 | 说明 | 建议 |
|------|------|------|
| config/ | 配置层（按环境拆分） | 敏感信息请使用 CI Secret 或 .env，不要入库 |
| core/ | 核心抽象与基础能力 | 稳定且覆盖全局能力，尽量写单元测试 |
| adapters/ | 第三方或技术实现 | 通过工厂/注册模式可替换实现 |
| extensions/ | 插件化扩展 | 放可选能力（多种执行器、数据源、断言器） |
| api/ | 业务接口封装（无实现细节） | 推荐同时提供 models/ 或 schemas/（Pydantic） |
| testcases/ | 测试用例（建议改名为 `tests/`） | 将 `conftest.py` 放到 `tests/conftest.py` 更符合惯例 |
| common/ | 通用工具函数 | 放通用工具，避免直接依赖业务模块 |
| reports/（建议新增） | 测试执行报告输出 | 支持 Allure / HTML 两种模式 |

---

## 关键改动建议（优先级）

1. 把 `testcases/` 重命名为 `tests/` 并移动 `conftest.py`（高）
2. 敏感信息不要入库，使用 CI Secret / `.env`（高）
3. 增加 `api/models/`（或 `schemas/`，使用 Pydantic）用于请求/响应校验（中）
4. adapters 插件化（通过工厂或注册机制实现可替换性）（中）
5. 增加 CI 配置（`.github/workflows/ci.yml`）：lint / type-check / pytest（中）
6. 在 `run_test.py` 中输出到 `reports/` 并支持 Allure（低）

---

## 快速上手（PowerShell）

创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

安装依赖：

```powershell
pip install -r requirements.txt
```

运行全部测试（如果使用 pytest）：

```powershell
pytest -q
```

通过统一入口运行（示例）：

```powershell
python run_test.py --env test
```

生成并查看 Allure 报告（示例）：

```powershell
pytest --alluredir=reports/allure-results
# 需要安装 allure 命令行工具：
allure serve reports/allure-results
```

---

## 我可以继续为你做的事情

- 我可以把 `testcases/` 自动重命名为 `tests/` 并移动 `conftest.py`（若你同意）；
- 我可以在仓库根创建 `docs/`、`reports/`、`api/models/` 等占位文件；
- 我可以添加一个 CI 工作流模板（`.github/workflows/ci.yml`）和一个简单的 `pyproject.toml`（可选）。

请告诉我你要我接着做哪一步，我会直接操作并验证。
