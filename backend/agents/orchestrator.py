# backend/agents/orchestrator.py
from .team_agent import TeamAgent
import logging

logging.basicConfig(level=logging.INFO)

class Orchestrator:
    """
    多轮博弈协调器，用于模拟两支国家队比赛。
    """

    def __init__(self, rounds: int = 5):
        self.rounds = rounds

    def simulate(self, home_team: dict, away_team: dict, formation_home: str, formation_away: str,
                 tactics_home: list, tactics_away: list, focus_players: dict) -> dict:
        """
        home_team, away_team: 球队完整信息字典
        formation_home/away: 阵型
        tactics_home/away: 战术列表
        focus_players: {"home":"核心球员","away":"核心球员"}
        """

        home_agent = TeamAgent()
        away_agent = TeamAgent()

        total_home_score = 0
        total_away_score = 0
        total_home_possession = 50
        history = []

        for r in range(1, self.rounds + 1):
            logging.info(f"=== 第 {r} 轮比赛 ===")

            home_context = {
                "my_team": home_team,
                "opponent_team": away_team,
                "formation": formation_home,
                "tactics": tactics_home,
                "focus_player": focus_players.get("home"),
                "opponent_focus_player": focus_players.get("away"),
                "round": r
            }
            home_resp = home_agent.act(home_context)

            away_context = {
                "my_team": away_team,
                "opponent_team": home_team,
                "formation": formation_away,
                "tactics": tactics_away,
                "focus_player": focus_players.get("away"),
                "opponent_focus_player": focus_players.get("home"),
                "round": r
            }
            away_resp = away_agent.act(away_context)

            # 更新比分和控球率
            total_home_score += home_resp.get("score_change", {}).get("home",0)
            total_away_score += away_resp.get("score_change", {}).get("away",0)

            total_home_possession += home_resp.get("possession_change",0) - away_resp.get("possession_change",0)
            total_home_possession = max(0, min(100, total_home_possession))
            total_away_possession = 100 - total_home_possession

            history.append({
                "round": r,
                "home_action": home_resp,
                "away_action": away_resp
            })

        final_result = {
            "score_probabilities":[
                {"score": f"{total_home_score}:{total_away_score}", "prob":100}
            ],
            "possession":{
                "home": total_home_possession,
                "away": total_away_possession
            },
            "tactical_analysis":"基于多轮博弈生成战术分析",
            "key_players": focus_players,
            "tactical_advice":"综合战术建议",
            "disclaimer":"本推演为 AI 模型基于历史数据模拟生成，仅供战术娱乐与学习参考，不代表实际比赛结果。",
            "history": history
        }

        return final_result