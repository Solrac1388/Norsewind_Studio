from fastapi import HTTPException, UploadFile
import os
import mimetypes
from typing import List

# Lista de tipos MIME permitidos para imÃ¡genes
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_image_file(file: UploadFile):
    """Valida que el archivo sea una imagen segura"""
    # Verificar tamaÃ±o
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="El archivo es demasiado grande")
    
    # Verificar tipo MIME
    content_type = file.content_type
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")
    
    return file

def validate_text_input(text: str, max_length: int = 500):
    """Valida que el texto de entrada sea seguro"""
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacÃ­o")
    
    if len(text) > max_length:
        raise HTTPException(status_code=400, detail=f"El texto excede el tamaÃ±o mÃ¡ximo de {max_length} caracteres")
    
    return text