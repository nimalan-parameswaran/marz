import chromadb
from backend.config import CHROMA_PATH

client = chromadb.PersistentClient(path=CHROMA_PATH)

def get_visit_collection():
    return client.get_or_create_collection(
        name="patient_visits",
        metadata={"hnsw:space": "cosine"}
    )