# agents/orchestrator.py
from agents.team_agent import TeamAgent
from agents.utils.qwen_client import QwenClient
import json

class MatchOrchestrator:
    """
    多轮球队博弈协调器
    """

    def __init__(self):
        self.home_agent = TeamAgent()
        self.away_agent = TeamAgent()
        self.final_client = QwenClient()  # 用于生成最终报告

    def run_match(self, home_team: dict, away_team: dict, rounds: int = 3):
        history = []

        home_msg = None
        away_msg = None

        for round_no in range(1, rounds + 1):
            # Home 发起
            home_msg = self.home_agent.analyze_team(
                home_team,
                away_team,
                round_no,
                previous_message=away_msg
            )
            history.append(home_msg)

            # Away 回复
            away_msg = self.away_agent.analyze_team(
                away_team,
                home_team,
                round_no,
                previous_message=home_msg
            )
            history.append(away_msg)

        # 最终汇总
        report = self.build_final_report(home_team, away_team, history)
        return report

    def build_final_report(self, home_team, away_team, history):
        """
        生成最终推演结果
        """
        prompt = f"""
根据以下球队博弈历史，生成最终比赛预测报告。
禁止讨论赌博。
禁止出现“必赢”“稳赢”等表述。
输出严格 JSON。

主队：{json.dumps(home_team, ensure_ascii=False)}
客队：{json.dumps(away_team, ensure_ascii=False)}

博弈记录：
{json.dumps(history, ensure_ascii=False)}

请返回：
{{
  "score_probability":[
    {{"score":"1-0","probability":24}},
    {{"score":"2-1","probability":21}},
    {{"score":"1-1","probability":19}}
  ],
  "possession":{{
    "{home_team['name']}": 52,
    "{away_team['name']}": 48
  }},
  "key_battles":["示例：Mbappe vs Walker"],
  "analysis":"战术分析示例...",
  "recommendation":"战术建议示例...",
  "disclaimer":"本推演为 AI 模型基于历史数据模拟生成，仅供战术娱乐与学习参考，不代表实际比赛结果。"
}}
"""
        client = QwenClient()
        return client.send(prompt)