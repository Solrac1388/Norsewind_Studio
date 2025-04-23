import os
import glob
import json
from PIL import Image
import numpy as np

def generate_metadata(avatars_dir, output_file):
    from ..services.embedding_service import EmbeddingService
    
    # Inicializar el servicio de embeddings
    embedding_service = EmbeddingService()
    embedding_service.initialize()
    
    # Definir categorías y opciones para clasificar
    categories = {
        "gender": ["male", "female", "non-binary"],
        "race": ["human", "elf", "dwarf", "orc", "undead", "demon", "angel"],
        "job": ["warrior", "mage", "archer", "rogue", "paladin", "priest", "necromancer", "bard"],
        "age": ["young", "adult", "middle-aged", "elderly"]
    }
    
    # Convertir edades descriptivas a números
    age_mapping = {"young": 20, "adult": 30, "middle-aged": 45, "elderly": 65}
    
    # Buscar imágenes de avatares
    image_files = glob.glob(os.path.join(avatars_dir, "*.jpg")) + \
                  glob.glob(os.path.join(avatars_dir, "*.png")) + \
                  glob.glob(os.path.join(avatars_dir, "*.jpeg"))
    
    print(f"Generando metadatos para {len(image_files)} avatares...")
    
    metadata = {}
    
    # Procesar cada imagen
    for img_path in image_files:
        filename = os.path.basename(img_path)
        avatar_meta = {}
        
        # Obtener embedding de la imagen
        img_embedding = embedding_service.get_image_embedding(img_path)
        
        # Clasificar para cada categoría
        for category, options in categories.items():
            best_match = None
            best_score = -1
            
            # Comparar la imagen con cada opción de la categoría
            for option in options:
                text = f"a {option} character"
                text_embedding = embedding_service.get_text_embedding(text)
                
                # Calcular similitud coseno
                similarity = float(np.dot(img_embedding, text_embedding))
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = option
            
            # Guardar el mejor resultado
            if category == "age":
                avatar_meta[category] = age_mapping[best_match]
            else:
                avatar_meta[category] = best_match
        
        metadata[filename] = avatar_meta
        print(f"Generado metadatos para {filename}: {avatar_meta}")
    
    # Guardar metadatos en un archivo JSON
    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadatos generados y guardados en {output_file}")
    return metadata