# How to run（运行说明）

## 1. 创建虚拟环境并安装依赖
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```

## 2. 运行 smoke 测试
```powershell
python run.py -e test -m smoke
```

## 3. 使用 Allure 生成测试报告（可选，推荐用于漂亮的测试报告）
1) 安装 pytest 插件
```powershell
pip install allure-pytest
```

2) 在本机安装 Allure CLI（用于将 allure-results 渲染成 HTML）。在 Windows 上可以使用 Chocolatey：
```powershell
choco install allure -y
```
或者从 Allure 的 GitHub Releases 页面下载并解压到 PATH。

3) 运行 pytest 并输出 allure 中间结果（pytest.ini 已默认把结果写到 `reports/allure-results`）：
```powershell
pytest
# 或者只运行单个测试
pytest api_test_framework/testcases/full/test_get_user_info.py::test_get_user_info -vv
```

4) 使用 Allure CLI 查看或生成报告：
```powershell
# 临时查看（会启动本地服务器并自动打开浏览器）
allure serve reports/allure-results

# 或者生成静态报告到目录并打开
allure generate reports/allure-results -o reports/allure-report --clean
start '' 'reports\allure-report\index.html'
```

注意：CI 环境中通常不带 GUI，可以在 CI 中生成 `reports/allure-report` 目录并把该目录作为 artifact 上传。
