from datetime import datetime
from cassandra.query import SimpleStatement
from .database import cassandra_db
import logging
from cassandra import ConsistencyLevel

logger = logging.getLogger(__name__)

class LeaderboardService:
    @staticmethod
    async def get_player_stats(email: str, year: int):
        """Get player stats for a specific year"""
        try:
            query = SimpleStatement(
                "SELECT dungeon_id, avg_minutes FROM player_stats WHERE email = %s AND year = %s",
                consistency_level=ConsistencyLevel.LOCAL_QUORUM
            )
            
            rows = cassandra_db.session.execute(query, (email, year))
            
            result = []
            for row in rows:
                result.append({
                    "dungeon_id": row.dungeon_id,
                    "avg_minutes": row.avg_minutes
                })
                
            return result
        except Exception as e:
            logger.error(f"Failed to get player stats: {str(e)}")
            raise e
    
    @staticmethod
    async def get_hall_of_fame(country: str, dungeon_id: int):
        """Get hall of fame for a specific country and dungeon"""
        try:
            now = datetime.now()
            current_year = now.year
            current_month = now.month
            
            # Get the last 4 months
            months = []
            for i in range(4):
                month = current_month - i
                year = current_year
                
                if month <= 0:
                    month += 12
                    year -= 1
                    
                months.append((year, month))
            
            results = []
            for year, month in months:
                query = SimpleStatement(
                    "SELECT email, user_name, minutes, date FROM hall_of_fame WHERE country = %s AND dungeon_id = %s AND year = %s AND month = %s LIMIT 5",
                    consistency_level=ConsistencyLevel.LOCAL_QUORUM
                )
                
                rows = cassandra_db.session.execute(query, (country, dungeon_id, year, month))
                
                for row in rows:
                    results.append({
                        "email": row.email,
                        "user_name": row.user_name,
                        "minutes": row.minutes,
                        "date": row.date.isoformat() if row.date else ""
                    })
            
            # Sort by minutes and take top 5
            results.sort(key=lambda x: x["minutes"])
            return results[:5]
        except Exception as e:
            logger.error(f"Failed to get hall of fame: {str(e)}")
            raise e
    
    @staticmethod
    async def get_horde_ranking(country: str, event_id: int):
        """Get horde ranking for a specific country and event"""
        try:
            query = SimpleStatement(
                "SELECT user_id, user_name, email, n_killed FROM horde_ranking WHERE event_id = %s AND country = %s LIMIT 50",
                consistency_level=ConsistencyLevel.ONE  # Menor consistencia para rankings de horda
            )
            
            rows = cassandra_db.session.execute(query, (event_id, country))
            
            result = []
            for row in rows:
                result.append({
                    "user_id": row.user_id,
                    "user_name": row.user_name,
                    "email": row.email,
                    "n_killed": row.n_killed
                })
                
            return result
        except Exception as e:
            logger.error(f"Failed to get horde ranking: {str(e)}")
            raise e
    
    @staticmethod
    async def record_dungeon_completion(email: str, dungeon_id: int, time_minutes: float, date_str: str):
        """Record a dungeon completion"""
        # Implementación del registro de completación de mazmorra
        # [Código de implementación para actualizar hall_of_fame y player_stats]
        pass
    
    @staticmethod
    async def record_monster_kill(email: str, event_id: int, monster_id: int):
        """Record a monster kill in a horde event"""
        # Implementación del registro de muertes de monstruos
        # [Código de implementación para actualizar horde_ranking]
        pass