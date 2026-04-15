
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection("medical_docs")

def search(query, k=5):
    emb = model.encode([query]).tolist()
    results = collection.query(query_embeddings=emb, n_results=k)
    return results["documents"][0]
