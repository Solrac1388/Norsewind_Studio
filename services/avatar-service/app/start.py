import os
import time
import redis
import subprocess
import sys
from app.scripts.load_avatars import load_avatars

def wait_for_redis():
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    max_retries = 30
    
    print(f"Esperando a que Redis ({redis_host}:{redis_port}) esté disponible...")
    
    for i in range(max_retries):
        try:
            client = redis.Redis(host=redis_host, port=redis_port)
            client.ping()
            client.close()
            print("Conexión a Redis establecida")
            return True
        except redis.exceptions.ConnectionError:
            print(f"Intento {i+1}/{max_retries}: Redis no disponible, reintentando en 2 segundos...")
            time.sleep(2)
    
    print("No se pudo conectar a Redis después de varios intentos")
    return False

def check_redis_has_avatars():
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    
    try:
        client = redis.Redis(host=redis_host, port=redis_port)
        avatar_keys = client.keys("avatar:*")
        client.close()
        return len(avatar_keys) > 0
    except Exception as e:
        print(f"Error verificando avatares en Redis: {str(e)}")
        return False

def generate_avatar_metadata():
    """Genera metadatos para los avatares"""
    try:
        avatars_dir = os.environ.get("AVATARS_DIR", "./assets/avatars")
        metadata_file = os.environ.get("METADATA_FILE", "./assets/metadata.json") or "./assets/metadata.json"
        
        # Verificar si ya existen metadatos
        if os.path.exists(metadata_file):
            with open(metadata_file) as f:
                existing_metadata = json.load(f)
            if existing_metadata:
                print(f"Usando archivo de metadatos existente: {metadata_file}")
                return True
        
        # Asegurar que exista el directorio para el archivo de metadatos
        os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
        
        print(f"Generando metadatos de avatares en: {metadata_file}")
        generate_metadata(avatars_dir, metadata_file)
        print("Metadatos generados correctamente")
        return True
    except Exception as e:
        print(f"Error al generar metadatos: {str(e)}")
        # Si hay un error en la generación de metadatos, creamos un archivo vacío
        # para que la carga de avatares continúe aunque sea con metadatos predeterminados
        try:
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
            with open(metadata_file, 'w') as f:
                json.dump({}, f)
        except:
            pass
        return False

def load_initial_avatars(force=False):
    # Código existente con ligera modificación para usar el archivo de metadatos por defecto
    has_avatars = check_redis_has_avatars()
    force_load = os.environ.get("LOAD_AVATARS_ON_STARTUP", "true").lower() == "true"
    
    if not has_avatars or force_load or force:
        print("Cargando avatares iniciales...")
        try:
            avatars_dir = os.environ.get("AVATARS_DIR", "./assets/avatars")
            metadata_file = os.environ.get("METADATA_FILE", "./assets/metadata.json") or "./assets/metadata.json"
            
            if not os.path.exists(avatars_dir):
                print(f"Directorio de avatares no encontrado: {avatars_dir}")
                return False
                
            load_avatars(avatars_dir, metadata_file)
            print("Avatares cargados correctamente")
            return True
        except Exception as e:
            print(f"Error al cargar avatares: {str(e)}")
            return False
    else:
        print("Redis ya tiene avatares cargados, omitiendo carga inicial")
    return True

if __name__ == "__main__":
    if not wait_for_redis():
        sys.exit(1)
    
    # Primero generamos metadatos, luego cargamos avatares
    generate_avatar_metadata()
    load_initial_avatars()
    
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"])