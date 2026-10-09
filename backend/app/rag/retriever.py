from sqlalchemy.orm import Session

from app.db.models import DocumentChunk
from app.ingestion.embedder import generate_embeddings


def retrieve_chunks(
    question: str,
    db: Session,
    document_id: int,
    top_k: int = 5
):
    # Convert the question into an embedding
    question_embedding = generate_embeddings([question])[0]

    # Calculate cosine distance
    distance = DocumentChunk.embedding.cosine_distance(question_embedding)

    results = (
        db.query(DocumentChunk, distance.label("distance"))
        .filter(DocumentChunk.document_id == document_id)
        .order_by(distance)
        .limit(top_k)
        .all()
    )

    # Keep only the DocumentChunk objects
    chunks = []

    for chunk, distance_value in results:
        print(
            f"Page {chunk.page_number} | "
            f"Distance: {distance_value:.4f}"
        )

        chunks.append(chunk)

    return chunks