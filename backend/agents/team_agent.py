# backend/agents/team_agent.py
from .base_agent import BaseAgent
import json

class TeamAgent(BaseAgent):
    """
    球队智能体，用于模拟一场比赛。
    每个智能体代表一支国家队。
    """

    SYSTEM_PROMPT = """
你是2026世界杯国家队智能体，任务是模拟本队比赛策略。
接收对阵信息，输出每轮行动、战术意图和比分变化。

输入 Context JSON：
{
    "my_team": { ...球队完整信息... },
    "opponent_team": { ...球队完整信息... },
    "formation": "4-3-3",
    "tactics": ["高位压迫","边路传中"],
    "focus_player": "本队核心球员",
    "opponent_focus_player": "对方核心球员",
    "round": 轮次编号
}

输出 JSON格式：
{
    "round": X,
    "action_summary": "本轮比赛动作总结",
    "possession_change": 正整数, 
    "score_change": {"home":0,"away":0},
    "notes": "战术意图说明"
}

规则：
1. 严格输出 JSON
2. 禁止使用“必中”“包赢”等词
3. 动作描述必须体现双方博弈
"""

    def act(self, context: dict) -> dict:
        """
        context: 包含 my_team, opponent_team, formation, tactics, focus_player, round
        """
        prompt = self.SYSTEM_PROMPT + "\nContext:\n" + json.dumps(context, ensure_ascii=False)
        # 调用 BaseAgent 的方法生成结构化 JSON
        resp = self.generate_response(prompt)

        # 尝试解析 JSON
        try:
            return json.loads(resp)
        except Exception:
            # 解析失败返回空占位，避免程序崩溃
            return {
                "round": context.get("round"),
                "action_summary": "AI未能生成动作",
                "possession_change": 0,
                "score_change": {"home":0,"away":0},
                "notes": ""
            }