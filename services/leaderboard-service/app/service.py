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
                consistency_level=ConsistencyLevel.ONE
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
                    consistency_level=ConsistencyLevel.ONE
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
                consistency_level=ConsistencyLevel.ONE
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
        try:
            # Parse date string
            date = datetime.fromisoformat(date_str)
            
            # Get user info from system_auth.roles (simplified example)
            user_query = SimpleStatement(
                "SELECT role FROM system_auth.roles WHERE role = %s",
                consistency_level=ConsistencyLevel.ONE
            )
            user_rows = cassandra_db.session.execute(user_query, (email,))
            user_name = email.split('@')[0]  # Fallback if user not found
            for user_row in user_rows:
                user_name = user_row.role
            
            # Get current year and month
            year = date.year
            month = date.month
            
            # Get country (simplified example - would come from user data)
            country = "global"  # Default value
            
            # Insert into hall_of_fame
            hall_query = SimpleStatement(
                """
                INSERT INTO hall_of_fame 
                (country, dungeon_id, year, month, email, user_name, minutes, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                consistency_level=ConsistencyLevel.ONE
            )
            
            cassandra_db.session.execute(
                hall_query, 
                (country, dungeon_id, year, month, email, user_name, time_minutes, date)
            )
            
            # Update player stats - first get current stats if they exist
            stats_query = SimpleStatement(
                """
                SELECT avg_minutes, completed_count 
                FROM player_stats 
                WHERE email = %s AND year = %s AND dungeon_id = %s
                """,
                consistency_level=ConsistencyLevel.ONE
            )
            
            stats_rows = cassandra_db.session.execute(stats_query, (email, year, dungeon_id))
            
            avg_minutes = time_minutes
            completed_count = 1
            
            # Calculate new average if stats exist
            for stats_row in stats_rows:
                if stats_row.completed_count is not None:
                    old_avg = stats_row.avg_minutes
                    old_count = stats_row.completed_count
                    completed_count = old_count + 1
                    avg_minutes = ((old_avg * old_count) + time_minutes) / completed_count
            
            # Update player stats
            update_stats_query = SimpleStatement(
                """
                UPDATE player_stats 
                SET avg_minutes = %s, completed_count = %s 
                WHERE email = %s AND year = %s AND dungeon_id = %s
                """,
                consistency_level=ConsistencyLevel.ONE
            )
            
            cassandra_db.session.execute(
                update_stats_query,
                (avg_minutes, completed_count, email, year, dungeon_id)
            )
            
            return True
        except Exception as e:
            logger.error(f"Failed to record dungeon completion: {str(e)}")
            raise e

    @staticmethod
    async def record_monster_kill(email: str, event_id: int, monster_id: int):
        """Record a monster kill in a horde event"""
        try:
            # Get user info
            user_query = SimpleStatement(
                "SELECT role FROM system_auth.roles WHERE role = %s",
                consistency_level=ConsistencyLevel.ONE
            )
            user_rows = cassandra_db.session.execute(user_query, (email,))
            
            user_name = email.split('@')[0]  # Fallback username
            user_id = abs(hash(email)) % (10**9)  # Generate consistent user_id from email
            
            for user_row in user_rows:
                user_name = user_row.role
            
            # Get country (simplified - would normally come from user profile)
            country = "global"
            
            # First check if user already has kills in this event
            check_query = SimpleStatement(
                """
                SELECT n_killed FROM horde_ranking 
                WHERE event_id = %s AND country = %s AND user_id = %s
                """,
                consistency_level=ConsistencyLevel.ONE
            )
            
            rows = cassandra_db.session.execute(check_query, (event_id, country, user_id))
            row = rows.one()
            
            n_killed = 1
            if row is not None:
                n_killed = row.n_killed + 1
            
            # Siempre insertar un nuevo registro con el count actualizado
            insert_query = SimpleStatement(
                """
                INSERT INTO horde_ranking 
                (event_id, country, user_id, user_name, email, n_killed) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                consistency_level=ConsistencyLevel.ONE
            )
            
            cassandra_db.session.execute(
                insert_query,
                (event_id, country, user_id, user_name, email, n_killed)
            )
            
            return True
        except Exception as e:
            logger.error(f"Failed to record monster kill: {str(e)}")
            raise e