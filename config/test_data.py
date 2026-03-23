"""
测试数据配置
根据不同环境加载不同的测试数据
"""
from config.settings import Config


class FrontierTestData:
    """Frontier接口测试数据"""

    # 测试环境数据（支持多个测试用例）
    TEST_ENV_DATA = [
        {
            "case_name": "测试用例1",
            "frontier_id": "8755128930300102590",
            "task_id": "9455361516900105533",
            "channel": "codatta-platform-website",
            "submission_data": {
                "task_id": "9455361516900105533",
                "data_submission": {
                    "taskId": "9455361516900105533",
                    "templateId": "AIRDROP_BAD_CASE_ANALYSIS",
                    "data": {
                        "model": "gemini-2.0-flash",
                        "question": "测试问题",
                        "model_answer": "测试答案",
                        "model_answer_screenshots": [{
                            "url": "https://file.b18a.io/388879687262208_997954_.png",
                            "hash": "8a39f46f5d7e0393ee2d21fc3255b70d34ba48bbd6b2dae0354ad026c09138b4"
                        }],
                        "error_analysis": "测试分析",
                        "category": "programming"
                    }
                }
            }
        },
        {
            "case_name": "测试用例2",
            "frontier_id": "8755128930300102590",
            "task_id": "9455361516900105533",
            "channel": "codatta-platform-website",
            "submission_data": {
                "task_id": "9455361516900105533",
                "data_submission": {
                    "taskId": "9455361516900105533",
                    "templateId": "AIRDROP_BAD_CASE_ANALYSIS",
                    "data": {
                        "model": "gemini-2.0-flash",
                        "question": "测试问题11",
                        "model_answer": "测试答案22",
                        "model_answer_screenshots": [{
                            "url": "https://file.b18a.io/388879687262208_997954_.png",
                            "hash": "8a39f46f5d7e0393ee2d21fc3255b70d34ba48bbd6b2dae0354ad026c09138b4"
                        }],
                        "error_analysis": "测试分析11",
                        "category": "programming"
                    }
                }
            }
        },
        {
            "case_name": "AIRDROP_KNOB测试",
            "frontier_id": "8755128930300102590",
            "task_id": "9513751347800105777",
            "channel": "codatta-platform-website",
            "submission_data": {
                "task_id": "9513751347800105777",
                "data_submission": {
                    "taskId": "9513751347800105777",
                    "templateId": "AIRDROP_KNOB",
                    "data": {
                        "original_image": "https://file.b18a.io/8478996582600109209_958803_.png",
                        "original_image_hash": "76c3b6d62ad55461af39835966d1f93a6336ae356d940022c45f1c5b6c36f759",
                        "annotated_image": "https://file.b18a.io/8478996582600109209_319302_.jpg",
                        "annotated_image_hash": "463a94827cf0e9abe44dd7b3938366377e27730cc1c9c2e8d7ea8f0e39d600b9",
                        "rect": {
                            "x1": 503, "y1": 229,
                            "x2": 778, "y2": 229,
                            "x3": 778, "y3": 505,
                            "x4": 503, "y4": 505,
                            "center": {"x": 641, "y": 367}
                        },
                        "pointer_point": {"x": 584, "y": 336},
                        "scale_value": "12112"
                    }
                }
            }
        },
    ]

    # 线上环境数据（支持多个测试用例）
    PROD_ENV_DATA = [
        {
            "case_name": "线上用例1",
            "frontier_id": "8780645457200101096",
            "task_id": "8780653218600101100",
            "channel": "codatta-platform-website",
            "submission_data": {
                "task_id": "8780653218600101100",
                "data_submission": {
                    "taskId": "8780653218600101100",
                    "templateId": "AIRDROP_BAD_CASE_ANALYSIS",
                    "data": {
                        "model": "claude-3.5-sonnet",
                        "question": "线上测试问题",
                        "model_answer": "线上测试答案",
                        "model_answer_screenshots": [{
                            "url": "https://file.b18a.io/7781137060500108043_107353_.png",
                            "hash": "d22a8c087843776459417bcd845a804df104b567ad4a957ebbcec2c99b451f2f"
                        }],
                        "error_analysis": "线上测试分析",
                        "category": "mathematics"
                    }
                }
            }
        },
    ]

    @classmethod
    def get_frontier_data(cls):
        """
        根据当前环境获取测试数据（返回所有测试用例）
        test/prod 环境从 TEST_ENV 环境变量读取
        """
        env = Config.ENV.lower()
        if env in ("prod", "production", "online"):
            return cls.PROD_ENV_DATA
        return cls.TEST_ENV_DATA

    @classmethod
    def get_all_cases(cls):
        """获取所有测试用例数据"""
        return cls.get_frontier_data()

    @classmethod
    def get(cls, key: str, default=None):
        """获取指定字段的测试数据（返回第一个用例）"""
        data_list = cls.get_frontier_data()
        if data_list:
            return data_list[0].get(key, default)
        return default
