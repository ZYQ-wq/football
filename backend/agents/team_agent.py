# agents/team_agent.py
from agents.base_agent import BaseAgent
import json

class TeamAgent(BaseAgent):
    """
    每支球队对应的智能体。
    """

    def analyze_team(
        self,
        team_context: dict,
        opponent_context: dict,
        round_no: int,
        previous_message: dict = None
    ):
        """
        模拟一轮博弈：
        team_context: 本队信息（含球员、阵型、战术、重点球员）
        opponent_context: 对手信息
        round_no: 当前轮次
        previous_message: 对手上一轮策略
        返回 JSON
        """
        prompt = f"""
你是国家队主教练。
禁止讨论赌博。
禁止出现“必赢”“稳赢”等表述。

本队信息：
{json.dumps(team_context, ensure_ascii=False)}

对手信息：
{json.dumps(opponent_context, ensure_ascii=False)}

当前博弈轮次：{round_no}
上一轮对手策略：
{json.dumps(previous_message, ensure_ascii=False)}

请严格返回 JSON，格式如下：
{{
  "team": "{team_context.get('name','')}",
  "offensive_plan": "",
  "defensive_plan": "",
  "key_player": "{team_context.get('focus_player','')}",
  "advantages": [],
  "risks": []
}}
"""
        return self.chat(prompt)