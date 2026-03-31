import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/marz")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "MedAIBase/MedGemma1.5:4b")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_data")