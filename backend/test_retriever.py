from app.db.session import SessionLocal
from app.rag.retriever import retrieve_chunks


db = SessionLocal()

question = "What is an embedded system?"

results = retrieve_chunks(question, db, top_k=5)

for result in results:
    print("Page:", result.page_number)
    print("Chunk:", result.chunk_index)
    print("Text:", result.text[:300])
    print("-" * 50)

db.close()