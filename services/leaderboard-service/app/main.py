from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

from .database import cassandra_db
from .models import (
    PlayerStatsResponse, HallOfFameResponse, HordeRankingResponse,
    DungeonCompletionRequest, MonsterKillRequest
)
from .service import LeaderboardService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Leaderboard Service API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Wait for Cassandra to be ready
    retries = 5
    for i in range(retries):
        if await cassandra_db.connect():
            break
        logger.warning(f"Failed to connect to Cassandra (attempt {i+1}/{retries}). Retrying in 5 seconds...")
        time.sleep(5)

@app.on_event("shutdown")
async def shutdown_event():
    await cassandra_db.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/statistics", response_model=PlayerStatsResponse)
async def get_player_stats(email: str, year: int):
    """Get player statistics for a specific email and year"""
    try:
        stats = await LeaderboardService.get_player_stats(email, year)
        return {"data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/halloffame", response_model=HallOfFameResponse)
async def get_hall_of_fame(country: str, dungeon_id: int):
    """Get hall of fame for a specific country and dungeon"""
    try:
        hall_of_fame = await LeaderboardService.get_hall_of_fame(country, dungeon_id)
        return {"data": hall_of_fame}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/horde/ranking", response_model=HordeRankingResponse)
async def get_horde_ranking(country: str, event_id: int):
    """Get horde ranking for a specific country and event"""
    try:
        ranking = await LeaderboardService.get_horde_ranking(country, event_id)
        return {"data": ranking}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/halloffame/record-completion")
async def record_dungeon_completion(request: DungeonCompletionRequest):
    """Record a dungeon completion"""
    try:
        success = await LeaderboardService.record_dungeon_completion(
            email=request.email,
            dungeon_id=request.dungeon_id,
            time_minutes=request.time_minutes,
            date_str=request.date
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/horde/record-kill")
async def record_monster_kill(request: MonsterKillRequest):
    """Record a monster kill in a horde event"""
    try:
        success = await LeaderboardService.record_monster_kill(
            email=request.email,
            event_id=request.event_id,
            monster_id=request.monster_id
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))