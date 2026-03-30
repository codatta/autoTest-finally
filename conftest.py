"""
Pytest配置文件
提供全局fixture和配置
"""
import pytest
import os
from datetime import datetime
from core.auth import Auth
from core.http_client import HttpClient
from api.user import UserApi
from api.frontier import FrontierApi
from api.checkin import CheckInApi
from api.quest import QuestApi
from config.settings import Config
from utils.email_sender import EmailSender

# ---------------------------------------------------------------------------
# 全局状态：判断是否"批量执行"（跑多个用例），单用例不发送邮件
# ---------------------------------------------------------------------------
_is_full_run = False
_last_report_path = None
_test_start_time = None
_test_stats = {"passed": 0, "failed": 0, "total": 0}  # 记录测试结果

def cleanup_old_reports(report_dir: str, max_count: int = None):
    """
    清理旧报告，只保留最新的N个报告

    Args:
        report_dir: 报告目录
        max_count: 最大保留报告数量
    """
    # 先确保目录存在（新增：避免目录不存在时报错）
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)
        return

    # 获取所有报告文件，按修改时间排序
    report_files = [
        os.path.join(report_dir, f)
        for f in os.listdir(report_dir)
        if f.endswith(".html")
    ]
    report_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # 删除超出数量的旧报告
    if max_count and len(report_files) > max_count:
        old_reports = report_files[max_count:]
        for old_report in old_reports:
            os.remove(old_report)
            print(f"已删除旧报告: {os.path.basename(old_report)}")


def pytest_collection_modifyitems(config, items):
    """
    收集完所有用例后调用。
    如果收集到 2 个及以上用例，说明是"批量执行"，最后才发邮件。
    """
    global _is_full_run
    if len(items) >= 5:
        _is_full_run = True
        print(f"\n[INFO] Detected batch execution ({len(items)} test cases), email report will be sent after test completion\n")


def pytest_runtest_logreport(report):
    """
    每个测试用例执行完后都会调用，记录通过/失败数量。
    """
    global _test_stats
    if report.when == "call":  # 只统计测试实际执行阶段，不统计 setup/teardown
        _test_stats["total"] += 1
        if report.passed:
            _test_stats["passed"] += 1
        elif report.failed:
            _test_stats["failed"] += 1

def pytest_configure(config):
    """pytest启动时的配置"""
    global _test_start_time, _last_report_path

    _test_start_time = datetime.now()

    # 1. 设置环境变量
    if not os.getenv("PRIVATE_KEY"):
        os.environ["PRIVATE_KEY"] = "0x40e68d7c277fbbd3399e7568011ec02cdb5f1009c1db15d883ef51bb41deb028"
    if not os.getenv("BASE_URL"):
        os.environ["BASE_URL"] = "https://app-test.b18a.io"

    # 2. 自动添加HTML报告参数（如果未手动指定）
    # 直接检查pytest-html插件的内置参数，不重复注册
    html_path = config.getoption("--html")
    if not html_path:
        # 创建报告目录（优化：明确拼接绝对路径，兼容不同执行环境）
        report_dir = os.path.join(os.path.abspath(os.getcwd()), "reports")
        # 强制创建目录（exist_ok=True：已存在时不报错）
        os.makedirs(report_dir, exist_ok=True)

        # 生成带时间戳的报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{timestamp}.html"
        report_path = os.path.join(report_dir, report_filename)

        # 直接设置内置的html报告参数（避免重复注册）
        setattr(config.option, "htmlpath", report_path)
        setattr(config.option, "self_contained_html", True)
        _last_report_path = report_path

        print(f"\n=== 报告将生成到: {report_path} ===\n")
        # 清理旧报告
        cleanup_old_reports(report_dir, Config.MAX_REPORT_COUNT)


def pytest_sessionfinish(session, exitstatus):
    """
    所有测试执行完毕后的钩子。
    仅在批量执行 + 邮件功能开启时才发送邮件。
    """
    global _is_full_run, _last_report_path, _test_start_time

    # 单用例执行，不发邮件
    if not _is_full_run:
        return

    # 邮件功能未启用
    if not Config.EMAIL_ENABLED:
        print("\n[INFO] Email is not enabled (EMAIL_ENABLED=false), skip sending email")
        return

    # 获取测试统计信息（从 pytest_runtest_logreport 记录的）
    passed = _test_stats["passed"]
    failed = _test_stats["failed"]
    total = _test_stats["total"]

    # 计算执行时长
    duration_str = "N/A"
    if _test_start_time:
        delta = datetime.now() - _test_start_time
        total_seconds = int(delta.total_seconds())
        m, s = divmod(total_seconds, 60)
        h, m = divmod(m, 60)
        duration_str = f"{h}h {m}m {s}s" if h else f"{m}m {s}s"

    # 找最新的 HTML 报告（优化：增加多层校验，避免None）
    report_path = _last_report_path
    if not report_path or not os.path.exists(report_path):
        report_dir = os.path.join(os.path.abspath(os.getcwd()), "reports")
        os.makedirs(report_dir, exist_ok=True)  # 再次确保目录存在
        files = [
            os.path.join(report_dir, f)
            for f in os.listdir(report_dir)
            if f.endswith(".html")
        ]
        if files:
            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            report_path = files[0]
        else:
            report_path = None  # 明确赋值，避免后续报错

    # 构建邮件内容（提前处理report_path为空的情况）
    subject = f"Test Report - {'All Passed' if failed == 0 else f'{failed} Failed'} ({datetime.now().strftime('%Y-%m-%d %H:%M')})"

    sender = EmailSender(
        host=Config.EMAIL_HOST,
        port=Config.EMAIL_PORT,
        user=Config.EMAIL_HOST_USER,
        password=Config.EMAIL_HOST_PASSWORD,
        use_tls=Config.EMAIL_USE_TLS,
        from_name=Config.EMAIL_FROM or Config.EMAIL_HOST_USER,
    )

    # 新增：调用build_test_report_html前，先校验report_path
    try:
        html_body = sender.build_test_report_html(
            report_path=report_path,
            passed=passed,
            failed=failed,
            total=total,
            duration=duration_str,
        )
    except Exception as e:
        # 捕获报告构建失败的异常，避免脚本终止
        print(f"\n[WARNING] Failed to build email report: {str(e)}")
        # 生成降级的邮件内容
        html_body = f"""
        <h2>接口自动化测试报告</h2>
        <p>执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>总用例数: {total} | 通过: {passed} | 失败: {failed}</p>
        <p>执行时长: {duration_str}</p>
        <p>[WARNING] Test report file generation failed, cannot display details</p>
        """

    # 收件人列表（支持多个，逗号分隔）
    to_list = [e.strip() for e in Config.EMAIL_TO.split(",") if e.strip()]

    # 附件（增加空值判断）
    attachments = [report_path] if (report_path and os.path.exists(report_path)) else []

    print("\n" + "=" * 50)
    try:
        sender.send(
            to_emails=to_list,
            subject=subject,
            html_body=html_body,
            attachments=attachments,
        )
        print("[INFO] Test report email sent successfully!")
    except Exception as e:
        print(f"[ERROR] Email sending failed: {str(e)}")
    print("=" * 50)

# 以下fixture代码保持不变
@pytest.fixture(scope="session")
def private_key():
    """获取私钥"""
    return os.getenv("PRIVATE_KEY")


@pytest.fixture(scope="session")
def auth(private_key):
    """
    创建认证实例（session级别，整个测试会话只登录一次）
    """
    print(f"\n=== 初始化认证，登录获取token ===")
    auth_instance = Auth(private_key=private_key)
    token = auth_instance.login()
    print(f"=== 登录成功，token: {token[:50]}... ===")
    return auth_instance


@pytest.fixture(scope="session")
def token(auth):
    """
    获取token（session级别）
    """
    return auth.get_token()


@pytest.fixture(scope="session")
def client(auth):
    """
    获取已认证的HTTP客户端（session级别）
    """
    return auth.get_client()


@pytest.fixture(scope="session")
def user_api(client):
    """
    获取用户API实例
    """
    return UserApi(client)


@pytest.fixture(scope="session")
def frontier_api(client):
    """
    获取Frontier API实例
    """
    return FrontierApi(client)


@pytest.fixture(scope="session")
def checkin_api(client):
    """
    获取签到API实例
    """
    return CheckInApi(client)


@pytest.fixture(scope="session")
def quest_api(client):
    """
    获取Quest API实例
    """
    return QuestApi(client)


@pytest.fixture
def fresh_client(auth):
    """
    获取新的HTTP客户端（function级别，每次测试都新建）
    """
    return auth.get_client()


@pytest.fixture
def fresh_user_api(auth):
    """
    获取新的用户API实例（function级别）
    """
    client = auth.get_client()
    return UserApi(client)
