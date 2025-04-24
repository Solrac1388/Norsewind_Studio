import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
from cassandra.policies import RoundRobinPolicy
import logging
from .config import CASSANDRA_CONTACT_POINTS, CASSANDRA_PORT, CASSANDRA_KEYSPACE, REPLICATION_FACTOR

logger = logging.getLogger(__name__)

class CassandraDB:
    def __init__(self):
        self.keyspace = CASSANDRA_KEYSPACE
        self.contact_points = CASSANDRA_CONTACT_POINTS.split(",")
        self.port = CASSANDRA_PORT
        self.cluster = None
        self.session = None
        
    async def connect(self):
        """Connect to Cassandra cluster and initialize session"""
        try:
            self.cluster = Cluster(
                self.contact_points, 
                port=self.port,
                load_balancing_policy=RoundRobinPolicy(),
                protocol_version=5  # Establecer explícitamente la versión del protocolo
            )
            self.session = self.cluster.connect()
            
            # Create keyspace if it doesn't exist
            self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
                WITH REPLICATION = {{
                    'class': 'SimpleStrategy',
                    'replication_factor': {REPLICATION_FACTOR}
                }}
            """)
            
            # Set keyspace
            self.session.set_keyspace(self.keyspace)
            
            # Crear tablas directamente
            self.session.execute("""
            CREATE TABLE IF NOT EXISTS hall_of_fame (
              country text,
              dungeon_id int,
              year int,
              month int,
              email text,
              user_name text,
              minutes float,
              date timestamp,
              PRIMARY KEY ((country, dungeon_id, year, month), minutes, email)
            ) WITH CLUSTERING ORDER BY (minutes ASC)
            """)
            
            self.session.execute("""
            CREATE TABLE IF NOT EXISTS player_stats (
              email text,
              year int,
              dungeon_id int,
              avg_minutes float,
              completed_count int,
              PRIMARY KEY ((email, year), dungeon_id)
            )
            """)
            
            try:
                self.session.execute("DROP TABLE IF EXISTS horde_ranking")
            except Exception as e:
                logger.warning(f"Error dropping horde_ranking table: {str(e)}")
            
            self.session.execute("""
            CREATE TABLE IF NOT EXISTS horde_ranking (
              event_id int,
              country text,
              user_id int,
              user_name text,
              email text,
              n_killed int,
              PRIMARY KEY ((event_id, country), user_id)
            )
            """)
            
            logger.info("Tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Cassandra cluster: {str(e)}")
            return False
    
    async def execute_cql_file(self, file_path):
        """Execute CQL commands from file"""
        try:
            with open(file_path, 'r') as f:
                cql_content = f.read()
                
            # Dividir por comandos (terminados en ;)
            commands = [cmd.strip() for cmd in cql_content.split(';') if cmd.strip()]
            
            for cmd in commands:
                # Ignorar comentarios y USE keyspace
                if cmd.startswith('--') or cmd.upper().startswith('USE'):
                    continue
                self.session.execute(cmd)
                
            return True
        except Exception as e:
            logger.error(f"Failed to execute CQL file {file_path}: {str(e)}")
            raise e
    
    async def execute(self, query, params=None, consistency_level=None):
        """Execute a CQL query with parameters and consistency level"""
        try:
            if consistency_level:
                query = SimpleStatement(query, consistency_level=consistency_level)
            
            return self.session.execute(query, params)
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise e
    
    async def execute_async(self, query, params=None, consistency_level=None):
        """Execute a CQL query asynchronously with parameters and consistency level"""
        try:
            if consistency_level:
                query = SimpleStatement(query, consistency_level=consistency_level)
            
            future = self.session.execute_async(query, params)
            return await future
        except Exception as e:
            logger.error(f"Async query execution failed: {str(e)}")
            raise e
    
    async def close(self):
        """Close connection to Cassandra cluster"""
        if self.cluster:
            self.cluster.shutdown()
            logger.info("Closed connection to Cassandra cluster")

# Singleton instance
cassandra_db = CassandraDB()