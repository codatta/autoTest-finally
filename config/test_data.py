"""
测试数据配置
根据不同环境加载不同的测试数据
"""
import random
import string
from config.settings import Config


# 封装随机内容生成工具函数（复用性更高）
def generate_random_str(length: int = 6) -> str:
    """生成随机字母+数字组合的字符串"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def generate_random_number(min_num: int = 1000, max_num: int = 9999) -> int:
    """生成指定范围的随机整数"""
    return random.randint(min_num, max_num)


class FrontierTestData:
    """Frontier接口测试数据"""

    # 基础测试数据模板（提取固定部分，动态字段留空）
    @classmethod
    def _get_test_env_template(cls):
        """测试环境数据模板（动态字段后续填充随机值）"""
        random_suffix = generate_random_str(8)  # 全局随机后缀，保证同用例内字段一致性
        random_num = generate_random_number()   # 随机数字

        return [
            {
                "case_name": f"测试用例1_{random_suffix}",
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
                            "question": f"测试问题_{random_suffix}_{random_num}",  # 随机化
                            "model_answer": f"测试答案_{random_suffix}_{random_num}",  # 随机化
                            "model_answer_screenshots": [{
                                "url": "https://file.b18a.io/388879687262208_997954_.png",
                                "hash": "8a39f46f5d7e0393ee2d21fc3255b70d34ba48bbd6b2dae0354ad026c09138b4"
                            }],
                            "error_analysis": f"测试分析_{random_suffix}_{random_num}",  # 随机化
                            "category": "programming"
                        }
                    }
                }
            },
            {
                "case_name": f"测试用例2_{random_suffix}",
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
                            "question": f"测试问题11_{random_suffix}_{random_num + 1}",  # 随机化
                            "model_answer": f"测试答案22_{random_suffix}_{random_num + 1}",  # 随机化
                            "model_answer_screenshots": [{
                                "url": "https://file.b18a.io/388879687262208_997954_.png",
                                "hash": "8a39f46f5d7e0393ee2d21fc3255b70d34ba48bbd6b2dae0354ad026c09138b4"
                            }],
                            "error_analysis": f"测试分析11_{random_suffix}_{random_num + 1}",  # 随机化
                            "category": "programming"
                        }
                    }
                }
            },
            {
                "case_name": f"AIRDROP_KNOB测试_{random_suffix}",
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
                            "scale_value": f"12112{random_num}"  # 随机化数值后缀
                        }
                    }
                }
            },
        ]

    # 线上环境数据模板（同理可随机化）
    @classmethod
    def _get_prod_env_template(cls):
        random_suffix = generate_random_str(8)
        random_num = generate_random_number()
        return [
            {
                "case_name": f"线上用例1_{random_suffix}",
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
                            "question": f"线上测试问题_{random_suffix}_{random_num}",  # 随机化
                            "model_answer": f"线上测试答案_{random_suffix}_{random_num}",  # 随机化
                            "model_answer_screenshots": [{
                                "url": "https://file.b18a.io/7781137060500108043_107353_.png",
                                "hash": "d22a8c087843776459417bcd845a804df104b567ad4a957ebbcec2c99b451f2f"
                            }],
                            "error_analysis": f"线上测试分析_{random_suffix}_{random_num}",  # 随机化
                            "category": "mathematics"
                        }
                    }
                }
            },
        ]

    @classmethod
    def get_frontier_data(cls):
        """
        根据当前环境获取测试数据（返回所有测试用例，动态生成随机内容）
        test/prod 环境从 TEST_ENV 环境变量读取
        """
        env = Config.ENV.lower()
        if env in ("prod", "production", "online"):
            return cls._get_prod_env_template()  # 线上环境也随机化
        return cls._get_test_env_template()     # 测试环境随机化

    @classmethod
    def get_all_cases(cls):
        """获取所有测试用例数据（动态生成）"""
        return cls.get_frontier_data()

    @classmethod
    def get(cls, key: str, default=None):
        """获取指定字段的测试数据（返回第一个用例）"""
        data_list = cls.get_frontier_data()
        if data_list:
            return data_list[0].get(key, default)
        return default