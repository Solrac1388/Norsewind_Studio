import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np
import io

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.processor = None
        
    def initialize(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        print("CLIP model initialized")
        
    def get_image_embedding(self, image_data):
        if isinstance(image_data, str):
            image = Image.open(image_data).convert("RGB")
        elif isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
        else:
            image = image_data
            
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            
        image_embedding = image_features.squeeze().numpy().astype(np.float32)
        image_embedding = image_embedding / np.linalg.norm(image_embedding)
        
        return image_embedding
        
    def get_text_embedding(self, text):
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            
        text_embedding = text_features.squeeze().numpy().astype(np.float32)
        text_embedding = text_embedding / np.linalg.norm(text_embedding)
        
        return text_embedding