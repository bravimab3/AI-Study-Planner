from app.db.session import SessionLocal
from app.db.models import Document
from app.ingestion.ingest import ingest_document


db = SessionLocal()

document = db.query(Document).first()

if document is None:
    print("No document found")
else:
    count = ingest_document(
        document_id=document.id,
        file_path=document.file_path,
        db=db
    )

    print("Ingestion completed")
    print("Chunks stored:", count)

db.close()