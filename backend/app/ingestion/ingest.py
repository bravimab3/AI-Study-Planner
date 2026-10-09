from sqlalchemy.orm import Session

from app.db.models import DocumentChunk
from app.ingestion.parsers import extract_text_from_pdf
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import generate_embeddings


def ingest_document(
    document_id: int,
    file_path: str,
    db: Session
):
    pages = extract_text_from_pdf(file_path)
    chunks = chunk_pages(pages)

    BATCH_SIZE = 20

    for i in range(0, len(chunks), BATCH_SIZE):

        batch = chunks[i:i + BATCH_SIZE]

        # Check which chunks are already stored
        new_batch = []

        for chunk in batch:
            existing = (
                db.query(DocumentChunk)
                .filter(
                    DocumentChunk.document_id == document_id,
                    DocumentChunk.chunk_index == chunk["chunk_index"],
                    DocumentChunk.page_number == chunk["page_number"]
                )
                .first()
            )

            if existing is None:
                new_batch.append(chunk)

        # If this batch is already stored, skip it
        if not new_batch:
            print(f"Skipping {min(i + BATCH_SIZE, len(chunks))}/{len(chunks)} chunks")
            continue

        texts = [chunk["text"].replace("\x00", "") for chunk in new_batch]

        embeddings = generate_embeddings(texts)

        for chunk, embedding in zip(new_batch, embeddings):

            document_chunk = DocumentChunk(
                document_id=document_id,
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"],
                text=chunk["text"].replace("\x00", ""),
                embedding=embedding
            )

            db.add(document_chunk)

        # Save this batch immediately
        db.commit()

        print(f"Processed {min(i + BATCH_SIZE, len(chunks))}/{len(chunks)} chunks")

    return len(chunks)