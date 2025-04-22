import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io

from .services.embedding_service import EmbeddingService
from .services.redis_service import RedisService
from .security.validators import validate_image_file, validate_text_input

app = FastAPI(title="Avatar Service API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_service = EmbeddingService()
redis_service = RedisService(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379))
)

@app.on_event("startup")
async def startup():
    embedding_service.initialize()
    redis_service.connect()
    redis_service.create_vector_index()

@app.on_event("shutdown")
async def shutdown():
    redis_service.close()

@app.post("/search/image")
async def search_by_image(file: UploadFile = File(...), top_k: int = Form(5)):
    try:
        file = validate_image_file(file)
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        embedding = embedding_service.get_image_embedding(image)
        
        similar_avatars = redis_service.find_similar_avatars(embedding, top_k)
        
        return JSONResponse(content=similar_avatars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/text")
async def search_by_text(description: str = Form(...), top_k: int = Form(5)):
    try:
        description = validate_text_input(description)
        
        embedding = embedding_service.get_text_embedding(description)
        
        similar_avatars = redis_service.find_similar_avatars(embedding, top_k)
        
        return JSONResponse(content=similar_avatars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/load-avatars")
async def run_load_avatars(password: str = Form(...)):
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin")
    if password != admin_password:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        from .scripts.load_avatars import load_avatars
        avatars_dir = os.environ.get("AVATARS_DIR", "./assets/avatars")
        metadata_file = os.environ.get("METADATA_FILE", "./assets/metadata.json")
        
        load_avatars(avatars_dir, metadata_file)
        return {"status": "success", "message": "Avatars loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}