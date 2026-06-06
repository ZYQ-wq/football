# backend/routers/simulate.py
from fastapi import APIRouter
from pydantic import BaseModel
from ..agents.orchestrator import Orchestrator
from ..data.teams import TEAMS  # 这里假设你已经导入球队完整信息字典

router = APIRouter()

class MatchRequest(BaseModel):
    home_team_id: str
    away_team_id: str
    formation_home: str
    formation_away: str
    tactics_home: list[str]
    tactics_away: list[str]
    focus_player_home: str
    focus_player_away: str

@router.post("/simulate")
def simulate_match(req: MatchRequest):
    home_team = TEAMS.get(req.home_team_id)
    away_team = TEAMS.get(req.away_team_id)

    if not home_team or not away_team:
        return {"error":"球队ID错误"}

    orchestrator = Orchestrator(rounds=5)
    result = orchestrator.simulate(
        home_team, away_team,
        req.formation_home, req.formation_away,
        req.tactics_home, req.tactics_away,
        {
            "home": req.focus_player_home,
            "away": req.focus_player_away
        }
    )

    return result