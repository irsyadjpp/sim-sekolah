import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_community.embeddings import OllamaEmbeddings # Ganti ke Ollama
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST", "localhost"),
    port=int(os.getenv("QDRANT_PORT", 6333))
)

# Gunakan model embedding lokal mxbai
# Model ini sangat bagus untuk mencari kemiripan makna secara offline
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

COLLECTION_NAME = "konteks_lokal"

def init_qdrant():
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)

    if not exists:
        print(f"🚀 Membuat koleksi lokal: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1024, # Ukuran untuk mxbai-embed-large adalah 1024
                distance=models.Distance.COSINE
            )
        )

def upsert_vector(chunk_id, text, sekolah_id):
    vector = embeddings.embed_query(text)
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "sekolah_id": sekolah_id,
                    "text": text,
                    "type": "knowledge_base"
                }
            )
        ]
    )
    print(f"✅ [Offline] Vector berhasil disimpan: {chunk_id}")