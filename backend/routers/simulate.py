# backend/routers/simulate.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from agents.orchestrator import MatchOrchestrator
from agents.utils.data_loader import load_team_by_id

router = APIRouter()

# ================= GET 接口，用于前端下拉框 =================
@router.get("/teams")
async def get_teams():
    return JSONResponse(content=[
        {"id":"france","name":"France"},
        {"id":"england","name":"England"},
        {"id":"brazil","name":"Brazil"},
        {"id":"argentina","name":"Argentina"},
        {"id":"spain","name":"Spain"},
        {"id":"germany","name":"Germany"},
        {"id":"portugal","name":"Portugal"},
        {"id":"japan","name":"Japan"}
    ])

@router.get("/formations")
async def get_formations():
    return JSONResponse(content=["4-3-3", "4-4-2", "3-5-2", "4-2-3-1"])

@router.get("/tactics")
async def get_tactics():
    return JSONResponse(content=["高位压迫", "防守反击", "控球", "边路突破", "快速反击"])
# ==========================================================

# ================= POST /simulate =================
@router.post("/simulate")
async def simulate_match(request: dict):
    """
    接收请求：
    {
        "home_team_id": "france",
        "away_team_id": "england",
        "formation": "4-3-3",
        "tactics": ["高位压迫", "边路突破"],
        "focus_home": "mbappe",
        "focus_away": "walker"
    }
    """
    try:
        home_team = load_team_by_id(request["home_team_id"])
        away_team = load_team_by_id(request["away_team_id"])

        home_team["formation"] = request.get("formation", "4-3-3")
        home_team["tactics"] = request.get("tactics", [])
        home_team["focus_player"] = request.get("focus_home", "")

        away_team["formation"] = request.get("formation", "4-3-3")
        away_team["tactics"] = request.get("tactics", [])
        away_team["focus_player"] = request.get("focus_away", "")

        orchestrator = MatchOrchestrator()
        result = orchestrator.run_match(home_team, away_team)

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})