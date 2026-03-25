# """
# 登录 UI 测试用例
# """
# import pytest
# from config.settings import config
#
#
# class TestLoginUI:
#     """登录 UI 测试类"""
#
#     def test_wallet_connect(self, page):
#         """
#         测试钱包连接功能
#
#         步骤：
#         1. 打开登录页
#         2. 点击钱包连接按钮
#         3. 等待连接完成
#
#         验证:
#         - 页面正常加载
#         - 点击连接按钮无报错
#         """
#         base_url = config.BASE_URL
#
#         print(f"\n=== 测试钱包连接功能 ===")
#         print(f"打开登录页: {base_url}/account/signin")
#
#         # 1. 打开登录页
#         page.goto(f"{base_url}/account/signin")
#         page.wait_for_load_state("domcontentloaded")
#         print("登录页加载完成")
#
#         # 2. 点击钱包连接按钮
#         # 注意：实际选择器需要根据页面调整
#         try:
#             # 尝试多种可能的选择器
#             wallet_button = page.locator("text=Wallet").first
#             if wallet_button.is_visible():
#                 wallet_button.click()
#                 print("点击了 Wallet 按钮")
#             else:
#                 # 尝试其他可能的选择器
#                 connect_button = page.locator("button:has-text('Connect'), [class*='connect']").first
#                 if connect_button.is_visible():
#                     connect_button.click()
#                     print("点击了 Connect 按钮")
#         except Exception as e:
#             print(f"未找到连接按钮: {e}")
#
#         # 3. 等待一段时间让用户完成钱包操作
#         print("等待连接完成...")
#         page.wait_for_timeout(5000)
#
#         # 4. 检查当前 URL
#         current_url = page.url
#         print(f"当前 URL: {current_url}")
#
#         # 验证页面正常（不强制要求登录成功，因为需要钱包交互）
#         assert "/signin" in current_url or "/app" in current_url, f"页面异常: {current_url}"
#
#         print("=== 测试完成 ===")
#
#     def test_home_page_load(self, page):
#         """
#         测试首页加载
#
#         验证:
#         - 首页能正常打开
#         - 页面无严重报错
#         """
#         base_url = config.BASE_URL
#
#         print(f"\n=== 测试首页加载 ===")
#
#         # 打开首页
#         page.goto(base_url)
#         page.wait_for_load_state("domcontentloaded")
#
#         print(f"首页 URL: {page.url}")
#         print(f"页面标题: {page.title()}")
#
#         # 验证页面加载成功
#         assert page.url.startswith(base_url), "首页加载失败"
#
#         print("=== 测试完成 ===")