"""
登录页面对象
"""
from playwright.sync_api import Page
from config.settings import config


class LoginPage:
    """登录页面"""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = config.BASE_URL

    def goto(self):
        """打开登录页"""
        self.page.goto(f"{self.base_url}/account/signin")

    def click_wallet_connect(self):
        """点击钱包连接按钮"""
        # 根据实际页面元素选择器进行调整
        self.page.click("text=Wallet", timeout=10000)

    def wait_for_connected(self, timeout: int = 30000):
        """等待连接成功"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def is_logged_in(self) -> bool:
        """检查是否登录成功"""
        current_url = self.page.url
        return "/app" in current_url or "/dashboard" in current_url

    def get_error_message(self) -> str:
        """获取错误信息"""
        error_selector = ".error, [class*='error'], [role='alert']"
        try:
            return self.page.locator(error_selector).first.text_content()
        except:
            return ""