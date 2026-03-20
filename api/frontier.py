"""
Frontier相关API接口
"""
from typing import Dict, Any, Optional
from core.http_client import HttpClient


class FrontierApi:
    """Frontier API"""

    def __init__(self, client: HttpClient):
        self.client = client

    def list(self, channel: str = "") -> Dict[str, Any]:
        """
        获取frontier列表

        Args:
            channel: 渠道标识

        Returns:
            API响应数据
        """
        response = self.client.post(
            "/api/v2/frontier/list",
            json_data={"channel": channel}
        )
        return self._parse_response(response)

    def submit_task(self, task_id: str, data_submission: Dict[str, Any]) -> Dict[str, Any]:
        """
        提交Frontier任务

        Args:
            task_id: 任务ID
            data_submission: 提交数据

        Returns:
            API响应数据
        """
        payload = {
            "task_id": task_id,
            "data_submission": data_submission
        }
        response = self.client.post(
            "/api/v2/frontier/task/submit",
            json_data=payload
        )
        return self._parse_response(response)

    def get_submission_list(self, frontier_id: str, page_size: int = 8, page_num: int = 1) -> Dict[str, Any]:
        """
        获取提交历史列表

        Args:
            frontier_id: Frontier项目ID
            page_size: 每页数量
            page_num: 页码

        Returns:
            API响应数据
        """
        payload = {
            "frontier_id": frontier_id,
            "page_size": page_size,
            "page_num": page_num
        }
        response = self.client.post(
            "/api/v2/submission/list",
            json_data=payload
        )
        return self._parse_response(response)

    def _parse_response(self, response) -> Dict[str, Any]:
        """统一解析响应，自动处理非JSON响应（如504超时）"""
        try:
            return response.json()
        except Exception:
            return {
                "_status_code": response.status_code,
                "_raw_text": response.text,
                "success": False,
                "errorMessage": f"HTTP {response.status_code}: {response.text[:200]}"
            }
