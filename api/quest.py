"""
Quest任务模块API
"""
from typing import Dict, Any
from core.http_client import HttpClient


class QuestApi:
    """Quest任务API"""

    def __init__(self, client: HttpClient):
        self.client = client

    def get_categories(self) -> Dict[str, Any]:
        """
        获取任务分类列表

        Returns:
            API响应数据（如果响应不是JSON，会附带 _status_code 字段）
        """
        response = self.client.post("/api/v2/task/categories")
        try:
            return response.json()
        except Exception:
            # 响应不是JSON（比如504超时），返回状态码和原始文本
            return {
                "_status_code": response.status_code,
                "_raw_text": response.text,
                "success": False,
                "errorMessage": f"HTTP {response.status_code}: {response.text[:200]}"
            }
