from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from typing import List, Dict, Any
import uuid


class qdrant_db():
    def __init__(self, url: str = "http://localhost:6333", 
                 collection_name: str = "agent_memory", 
                 vector_size: int = 8192,):
        
        self.client = QdrantClient(url=url)
        self.collection = collection_name
        self.vector_size = vector_size
