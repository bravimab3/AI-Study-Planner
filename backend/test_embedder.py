from app.ingestion.embedder import generate_embedding


text = "An embedded system is a computer system designed for a specific purpose."

embedding = generate_embedding(text)

print("Embedding generated successfully")
print("Vector length:", len(embedding))
print("First 5 values:", embedding[:5])