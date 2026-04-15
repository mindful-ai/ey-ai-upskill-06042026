
from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

doc = Document("medical_knowledge_dataset.docx")

paragraphs = [p.text for p in doc.paragraphs if len(p.text.strip()) > 50]

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection("medical_docs")

embeddings = model.encode(paragraphs).tolist()

# ChromaDB has a max batch size limit; process in chunks
BATCH_SIZE = 5461
total_docs = len(paragraphs)

for i in range(0, total_docs, BATCH_SIZE):
    batch_end = min(i + BATCH_SIZE, total_docs)
    batch_docs = paragraphs[i:batch_end]
    batch_embeddings = embeddings[i:batch_end]
    batch_ids = [str(j) for j in range(i, batch_end)]
    
    collection.add(
        documents=batch_docs,
        embeddings=batch_embeddings,
        ids=batch_ids
    )
    print(f"Ingested batch {i // BATCH_SIZE + 1}: documents {i} to {batch_end}")

print(f"Medical dataset ingested into ChromaDB ({total_docs} total documents)")
