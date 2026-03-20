"""
邮件发送模块
"""
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from typing import List


class EmailSender:
    """邮件发送器"""

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        use_tls: bool = True,
        from_name: str = None,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_tls = use_tls
        self.from_name = from_name or user

    def send(
        self,
        to_emails: List[str],
        subject: str,
        body: str = "",
        html_body: str = None,
        attachments: List[str] = None,
    ):
        """
        发送邮件

        Args:
            to_emails: 收件人列表
            subject: 邮件主题
            body: 纯文本邮件正文
            html_body: HTML 格式邮件正文（可选）
            attachments: 附件文件路径列表（可选）
        """
        if not to_emails:
            print("⚠️ 未配置收件人，跳过发送邮件")
            return

        # 构建邮件
        msg = MIMEMultipart("mixed")
        # 发件人：中文名称需要 RFC2047 编码
        from_header = Header(self.from_name, "utf-8")
        msg["From"] = f"{from_header} <{self.user}>"
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = Header(subject, "utf-8")

        # 添加正文
        if html_body:
            part_html = MIMEText(html_body, "html", "utf-8")
            msg.attach(part_html)
        if body:
            part_text = MIMEText(body, "plain", "utf-8")
            msg.attach(part_text)

        # 添加附件
        for file_path in (attachments or []):
            if not os.path.exists(file_path):
                print(f"⚠️ 附件文件不存在，跳过: {file_path}")
                continue

            with open(file_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)

                # 提取文件名
                filename = os.path.basename(file_path)
                part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=("utf-8", "", filename),
                )
                msg.attach(part)

        # 发送邮件
        try:
            if self.use_tls:
                # STARTTLS 方式（port 通常为 587）
                server = smtplib.SMTP(self.host, self.port, timeout=15)
                server.ehlo()
                server.starttls()
                server.ehlo()
            else:
                # SSL 方式（port 通常为 465）
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.host, self.port, context=context, timeout=15)
            server.login(self.user, self.password)
            server.sendmail(self.user, to_emails, msg.as_string())
            server.quit()
            print(f"\n✅ 邮件发送成功！")
            print(f"   收件人: {', '.join(to_emails)}")
            print(f"   主题: {subject}")
            for f in (attachments or []):
                print(f"   附件: {os.path.basename(f)}")
        except Exception as e:
            print(f"\n❌ 邮件发送失败: {e}")

    def build_test_report_html(self, report_path: str, passed: int, failed: int, total: int, duration: str) -> str:
        """
        构建测试报告邮件的 HTML 内容

        Args:
            report_path: 报告文件路径
            passed: 通过数量
            failed: 失败数量
            total: 总数量
            duration: 执行时长

        Returns:
            HTML 格式的邮件正文
        """
        status = "✅ 全部通过" if failed == 0 else f"❌ 有 {failed} 个用例失败"
        status_color = "#28a745" if failed == 0 else "#dc3545"

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333;">🧪 测试报告</h2>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f8f9fa;">
                        <strong>执行状态</strong>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; color: {status_color}; font-weight: bold;">
                        {status}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f8f9fa;">
                        <strong>用例统计</strong>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd;">
                        总计: {total} | ✅ 通过: {passed} | ❌ 失败: {failed}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f8f9fa;">
                        <strong>执行时长</strong>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{duration}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f8f9fa;">
                        <strong>报告文件</strong>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{os.path.basename(report_path)}</td>
                </tr>
            </table>

            <p style="color: #666; font-size: 12px;">
                此邮件由自动化测试框架自动发送，报告详情请查看附件 HTML 文件。
            </p>
        </body>
        </html>
        """
        return html
