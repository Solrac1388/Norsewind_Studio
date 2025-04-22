import redis
import numpy as np

class RedisService:
    def __init__(self, host="localhost", port=6379, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        
    def connect(self):
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=False
        )
        self.client.ping()
        print(f"Connected to Redis at {self.host}:{self.port}")
        
    def close(self):
        if self.client:
            self.client.close()
            print("Redis connection closed")
        
    def create_vector_index(self):
        try:
            embedding_dim = 512
            
            self.client.execute_command(
                "FT.CREATE", 
                "avatar_idx",
                "ON", "HASH",
                "PREFIX", "1", "avatar:",
                "SCHEMA",
                "avatar_id", "TEXT",
                "filename", "TEXT",
                "gender", "TEXT",
                "race", "TEXT", 
                "job", "TEXT",
                "age", "NUMERIC",
                "embedding", "VECTOR", "HNSW", "6", 
                    "TYPE", "FLOAT32",
                    "DIM", str(embedding_dim),
                    "DISTANCE_METRIC", "COSINE"
            )
            print("Vector index created")
            return True
        except redis.exceptions.ResponseError as e:
            if "Index already exists" in str(e):
                print("Index already exists")
                return True
            else:
                print(f"Error creating index: {str(e)}")
                return False
                
    def store_avatar(self, avatar_id, filename, gender, race, job, age, embedding):
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        self.client.hset(
            f"avatar:{avatar_id}",
            mapping={
                "avatar_id": str(avatar_id),
                "filename": filename,
                "gender": gender,
                "race": race,
                "job": job,
                "age": str(age),
                "embedding": embedding_bytes
            }
        )
        
    def find_similar_avatars(self, embedding, top_k=5):
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        query = f"*=>[KNN {top_k} @embedding $embedding AS score]"
        params = {"embedding": embedding_bytes}
        
        results = self.client.ft("avatar_idx").search(query, params).docs
        
        avatars = []
        for res in results:
            avatars.append({
                "id": res["avatar_id"],
                "filename": res["filename"],
                "gender": res["gender"],
                "race": res["race"],
                "job": res["job"],
                "age": int(res["age"]),
                "similarity": 1.0 - float(res["__embedding_score"])
            })
            
        return avatars
