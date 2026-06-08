# agents/utils/qwen_client.py
import os

class QwenClient:
    """
    通义千问 API 封装
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("QWEN_API_KEY", "")
        if not self.api_key:
            raise ValueError("请设置 QWEN_API_KEY")

    def send(self, prompt: str) -> str:
        """
        调用通义千问 API
        这里先用 Mock 返回，方便本地调试
        """
        # TODO: 替换为真实 API 请求
        print("==== Qwen Prompt ====")
        print(prompt)
        print("=====================")
        # Mock 返回
        return prompt  # 暂时直接返回 prompt 用于测试