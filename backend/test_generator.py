from app.db.session import SessionLocal
from app.rag.retriever import retrieve_chunks
from app.rag.generator import generate_answer


db = SessionLocal()

question = "What is an embedded system?"

chunks = retrieve_chunks(
    question,
    db,
    top_k=5
)

answer = generate_answer(
    question,
    chunks
)

print("\nANSWER:")
print(answer)

db.close()