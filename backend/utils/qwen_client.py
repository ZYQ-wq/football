import os
import requests
from backend.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

API_KEY = OPENAI_API_KEY
API_URL = OPENAI_BASE_URL

class QwenClient:
    """
    通义千问 API 调用封装
    """
    def __init__(self):
        self.api_key = API_KEY

    def chat(self, prompt: str) -> str:
        """
        发送 Prompt，返回模型文本
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen-plus-2025-07-28",
            "prompt": prompt,
            "max_tokens": 1000
        }
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data.get("text", "")
        except Exception as e:
            return f"Error: {str(e)}"