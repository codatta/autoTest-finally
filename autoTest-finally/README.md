# API 自动化测试框架

基于 Python + Pytest 的接口自动化测试框架，支持 Web3 钱包登录。

## 项目结构

```
autoTest/
├── config/              # 配置模块
│   ├── __init__.py
│   └── settings.py     # 配置管理
├── core/               # 核心模块
│   ├── __init__.py
│   ├── auth.py         # 认证管理（Web3登录）
│   ├── http_client.py  # HTTP客户端封装
│   └── signer.py       # Web3签名工具
├── api/                # API接口定义
│   ├── __init__.py
│   └── user.py         # 用户相关接口
├── tests/              # 测试用例
│   ├── __init__.py
│   ├── test_login.py   # 登录流程测试
│   └── test_user.py    # 用户接口测试
├── utils/              # 工具模块
│   ├── __init__.py
│   └── assertions.py   # 响应断言工具
├── conftest.py         # pytest配置
├── requirements.txt    # 依赖包
├── .env.example        # 环境变量示例
└── README.md           # 说明文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

### 方式1: 环境变量

在运行测试前设置环境变量：

```powershell
# Windows PowerShell
$env:BASE_URL="https://app-test.b18a.io"
$env:PRIVATE_KEY="0x40e68d7c277fbbd3399e7568011ec02cdb5f1009c1db15d883ef51bb41deb028"
```

### 方式2: .env 文件

复制 `.env.example` 为 `.env` 并修改配置：

```bash
copy .env.example .env
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行指定测试文件

```bash
# 运行登录测试
pytest tests/test_login.py

# 运行用户接口测试
pytest tests/test_user.py
```

### 运行指定测试用例

```bash
pytest tests/test_login.py::TestLogin::test_login_flow -v
```

### 生成HTML报告

```bash
pytest --html=report.html --self-contained-html
```

### 并行执行

```bash
pytest -n auto  # 自动使用CPU核心数
```

## 框架特性

### 1. 低耦合设计

- **配置模块 (config/)**: 集中管理配置，与业务逻辑分离
- **核心模块 (core/)**: 提供基础功能（HTTP、认证、签名）
- **API模块 (api/)**: 封装接口定义，便于维护和扩展
- **工具模块 (utils/)**: 提供通用工具函数

### 2. Token自动管理

- 登录接口自动获取token
- Token在session级别共享，避免重复登录
- HTTP客户端自动携带token

### 3. Web3钱包支持

- 支持私钥导入
- 自动生成符合EIP-191标准的签名
- 支持多种钱包（OKX Wallet等）

### 4. 简洁的断言

```python
from utils.assertions import assert_response

# 使用断言工具
result = user_api.get_user_info()
assert_response(result, success=True).has_key("data")
```

## 添加新接口

### 1. 在 api/ 目录下创建新的接口文件

```python
# api/example.py
from typing import Dict, Any
from core.http_client import HttpClient

class ExampleApi:
    def __init__(self, client: HttpClient):
        self.client = client

    def get_something(self) -> Dict[str, Any]:
        response = self.client.get("/api/v2/example/something")
        return response.json()
```

### 2. 在 conftest.py 中添加fixture

```python
@pytest.fixture
def example_api(client):
    from api.example import ExampleApi
    return ExampleApi(client)
```

### 3. 编写测试用例

```python
def test_example(example_api):
    result = example_api.get_something()
    assert result.get("success") is True
```

## 常见问题

### Q: 如何切换测试环境？

```bash
$env:BASE_URL="https://app-prod.b18a.io"
pytest
```

### Q: 如何使用新的私钥？

```bash
$env:PRIVATE_KEY="你的新私钥"
pytest
```

### Q: 如何调试查看详细日志？

```bash
pytest -s -v
```

## License

MIT
