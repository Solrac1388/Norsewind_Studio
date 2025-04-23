import os
import glob
import json
import uuid
import numpy as np

def load_avatars(avatars_dir, metadata_file=None):
    from ..services.embedding_service import EmbeddingService
    from ..services.redis_service import RedisService
    
    # Inicializar servicio de embeddings
    embedding_service = EmbeddingService()
    embedding_service.initialize()
    
    # Inicializar servicio de Redis
    redis_service = RedisService(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", 6379))
    )
    redis_service.connect()
    redis_service.create_vector_index()
    
    # Cargar metadatos existentes si hay un archivo
    metadata = {}
    if metadata_file and os.path.exists(metadata_file):
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                print(f"Metadatos cargados desde {metadata_file}")
        except:
            print(f"Error al cargar metadatos desde {metadata_file}, se generarán automáticamente")
    
    # Buscar imágenes de avatares
    image_files = glob.glob(os.path.join(avatars_dir, "*.jpg")) + \
                  glob.glob(os.path.join(avatars_dir, "*.png")) + \
                  glob.glob(os.path.join(avatars_dir, "*.jpeg"))
    
    print(f"Encontradas {len(image_files)} imágenes de avatares")
    
    # Opciones para clasificación automática con CLIP
    categories = {
        "gender": ["male", "female"],
        "race": ["human", "elf", "dwarf", "orc", "undead"],
        "job": ["warrior", "mage", "archer", "rogue", "paladin"]
    }
    age_ranges = {
        "young": 20,
        "adult": 30,
        "middle-aged": 45,
        "elderly": 60
    }
    
    # Limpiar avatares existentes en Redis
    for key in redis_service.client.keys("avatar:*"):
        redis_service.client.delete(key)
        
    # Procesar cada imagen
    for img_path in image_files:
        filename = os.path.basename(img_path)
        avatar_id = str(uuid.uuid4())
        
        # Verificar si ya tenemos metadatos para esta imagen
        avatar_meta = metadata.get(filename, None)
        
        # Si no hay metadatos para esta imagen, generarlos con CLIP
        if not avatar_meta:
            print(f"Generando metadatos para {filename}...")
            avatar_meta = {}
            
            # Obtener embedding de la imagen
            img_embedding = embedding_service.get_image_embedding(img_path)
            
            # Clasificar cada categoría
            for category, options in categories.items():
                best_match = None
                best_score = -1
                
                for option in options:
                    prompt = f"a {option} character"
                    text_embedding = embedding_service.get_text_embedding(prompt)
                    
                    # Calcular similitud
                    similarity = float(np.dot(img_embedding, text_embedding))
                    
                    if similarity > best_score:
                        best_score = similarity
                        best_match = option
                
                avatar_meta[category] = best_match
                print(f"  - {category}: {best_match}")
            
            # Clasificar edad
            best_age = None
            best_score = -1
            
            for age_desc, age_value in age_ranges.items():
                prompt = f"a {age_desc} character"
                text_embedding = embedding_service.get_text_embedding(prompt)
                
                similarity = float(np.dot(img_embedding, text_embedding))
                
                if similarity > best_score:
                    best_score = similarity
                    best_age = age_value
            
            avatar_meta["age"] = best_age
            print(f"  - age: {best_age}")
            
            # Guardar en el diccionario de metadatos
            metadata[filename] = avatar_meta
        
        # Obtener embedding para almacenar en Redis
        embedding = embedding_service.get_image_embedding(img_path)
        
        # Almacenar en Redis
        redis_service.store_avatar(
            avatar_id=avatar_id,
            filename=filename,
            gender=avatar_meta.get("gender", "unknown"),
            race=avatar_meta.get("race", "unknown"),
            job=avatar_meta.get("job", "unknown"),
            age=avatar_meta.get("age", 30),
            embedding=embedding
        )
        
        print(f"Avatar {filename} almacenado con ID {avatar_id}")
    
    # Guardar metadatos en archivo si se especificó uno
    if metadata_file:
        os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadatos guardados en {metadata_file}")
    
    redis_service.close()
    print(f"Cargados exitosamente {len(image_files)} avatares en Redis")