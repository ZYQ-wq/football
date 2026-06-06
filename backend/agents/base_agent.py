from utils.qwen_client import QwenClient
import json
import logging

logging.basicConfig(level=logging.INFO)

class BaseAgent:
    """
    智能体基类，封装通义千问 API 调用
    """
    def __init__(self, role_name: str):
        self.role_name = role_name
        self.client = QwenClient()
    
    def generate_response(self, prompt: str) -> dict:
        """
        调用通义千问 API 获取结构化 JSON 响应
        返回字典类型
        """
        logging.info(f"[{self.role_name}] 发送 Prompt: {prompt}")
        try:
            response_text = self.client.chat(prompt)
            logging.info(f"[{self.role_name}] 返回原始文本: {response_text}")
            # 尝试解析为 JSON
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            logging.error(f"[{self.role_name}] JSON解析失败，返回原始文本")
            return {"raw_text": response_text}