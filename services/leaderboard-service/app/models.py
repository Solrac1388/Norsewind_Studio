from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Modelos para respuestas
class DungeonStat(BaseModel):
    dungeon_id: int
    avg_minutes: float

class PlayerStatsResponse(BaseModel):
    data: List[DungeonStat]

class HallOfFameEntry(BaseModel):
    email: str
    user_name: str
    minutes: float
    date: str

class HallOfFameResponse(BaseModel):
    data: List[HallOfFameEntry]

class HordeRankingEntry(BaseModel):
    user_id: int
    user_name: str
    email: str
    n_killed: int

class HordeRankingResponse(BaseModel):
    data: List[HordeRankingEntry]

# Modelos para peticiones
class DungeonCompletionRequest(BaseModel):
    email: str
    dungeon_id: int
    time_minutes: float
    date: str

class MonsterKillRequest(BaseModel):
    email: str
    event_id: int
    monster_id: int