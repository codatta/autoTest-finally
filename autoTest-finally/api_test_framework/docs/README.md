# 项目结构（更清晰的展示）

下面是该 API 测试框架的结构说明，已精简为一目了然的目录树与关键文件说明，便于阅读和快速上手。

代码树（简洁版）

```
api_test_framework/
├─ docs/                     # 文档
│  ├─ README.md              # 项目结构与快速使用（中文）
│  └─ run.md                 # 运行说明与示例命令
├─ config/                   # 配置（按环境分离）
│  ├─ env/
│  │  ├─ test.yaml
│  │  ├─ staging.yaml
│  │  └─ prod.yaml
│  ├─ global.yaml
│  └─ .env.example
├─ core/                     # 核心基础能力（轻量）
├─ api/                      # 业务接口封装（模块化）
├─ testcases/                # pytest 用例与夹具
├─ utils/                    # 工具函数与测试辅助
├─ reports/                  # 测试报告（运行时生成）
├─ .github/workflows/        # CI 示例（可选）
├─ examples/                 # 简单示例脚本
├─ run.py                    # 统一运行入口
├─ requirements.txt
├─ pytest.ini
├─ Dockerfile
└─ LICENSE
```

关键文件说明（快速参考）

| 路径/文件 | 说明 |
|---|---|
| `config/env/*.yaml` | 按环境分离的 YAML 配置，存放 base_url、环境特有配置。|
| `config/global.yaml` | 全局配置（超时、重试次数、报告路径等）。|
| `core/config_loader.py` | 负责加载合并全局与环境配置（pydantic 或环境变量）。|
| `core/http_client.py` | HTTP 客户端封装（requests.Session），统一请求超时/重试策略。|
| `core/logger.py` | 日志工厂：全局统一格式输出。|
| `api/base_api.py` | 基类：封装常用请求方法，业务接口继承。|
| `api/*_api.py` | 各个业务模块（user/order/wallet 等）的接口封装。|
| `testcases/conftest.py` | pytest 全局夹具（config、client、会话级初始化）。|
| `testcases/smoke/` | 冒烟测试：快速保证核心流程可用。|
| `reports/` | 存放 pytest-html 或 Allure 输出的报告。|
| `run.py` | 统一入口脚本（支持 -e/--env、-m/--marker 等参数，触发 pytest）。|

简洁使用说明（PowerShell）

1) 在项目目录创建并激活虚拟环境，安装依赖：

```powershell
cd D:\pythonProject\autoTest-finally\api_test_framework
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) 快速验证（示例脚本）：

```powershell
python .\examples\simple_test_run.py
```

3) 运行冒烟测试（推荐临时方式：设置 `PYTHONPATH`）：

```powershell
$env:PYTHONPATH = "D:\\pythonProject\\autoTest-finally\\api_test_framework"
pytest testcases -m smoke --html=reports\report.html --self-contained-html
```

提示与推荐

- 若你希望无需每次设 `PYTHONPATH`：我可以为你添加 `pyproject.toml` 或 `setup.cfg`，并把包设为可编辑安装（`pip install -e .`）。
- 若想一键运行：我也可以修改 `run.py`，在调用 pytest 前自动设置 `PYTHONPATH`，运行体验会更好。

如需我把文档再转成 Markdown 中的折叠段或添加徽章（Badge）、示意图（PlantUML/mermaid），也可以告诉我你要的样式，我一并替换。
