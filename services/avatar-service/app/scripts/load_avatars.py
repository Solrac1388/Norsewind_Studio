import os
import glob
import json
import uuid
from ..services.embedding_service import EmbeddingService
from ..services.redis_service import RedisService

def load_avatars(avatars_dir, metadata_file=None):
    embedding_service = EmbeddingService()
    embedding_service.initialize()
    
    redis_service = RedisService(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", 6379))
    )
    redis_service.connect()
    
    redis_service.create_vector_index()
    
    metadata = {}
    if metadata_file and os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    
    image_files = glob.glob(os.path.join(avatars_dir, "*.jpg")) + \
                  glob.glob(os.path.join(avatars_dir, "*.png")) + \
                  glob.glob(os.path.join(avatars_dir, "*.jpeg"))
    
    print(f"Found {len(image_files)} avatar images")
    
    for img_path in image_files:
        filename = os.path.basename(img_path)
        avatar_id = str(uuid.uuid4())
        
        avatar_meta = metadata.get(filename, {})
        gender = avatar_meta.get("gender", "unknown")
        race = avatar_meta.get("race", "unknown")
        job = avatar_meta.get("job", "unknown")
        age = avatar_meta.get("age", 30)
        
        print(f"Generating embedding for {filename}")
        embedding = embedding_service.get_image_embedding(img_path)
        
        redis_service.store_avatar(
            avatar_id=avatar_id,
            filename=filename,
            gender=gender,
            race=race,
            job=job,
            age=age,
            embedding=embedding
        )
        print(f"Stored avatar {filename} with ID {avatar_id}")
    
    redis_service.close()
    print(f"Successfully loaded {len(image_files)} avatars into Redis")