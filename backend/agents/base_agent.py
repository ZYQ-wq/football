# agents/base_agent.py
import os
import json
from .utils.qwen_client import QwenClient

class BaseAgent:
    """封装通义千问 API 调用"""

    def __init__(self):
        api_key = os.getenv("QWEN_API_KEY", "")
        if not api_key:
            raise ValueError("请在环境变量中设置 QWEN_API_KEY")
        self.client = QwenClient(api_key)

    def chat(self, prompt: str):
        """发送 Prompt 给 LLM，并返回 JSON"""
        response = self.client.send(prompt)
        try:
            # 尝试解析 JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果失败，直接返回原文
            return response