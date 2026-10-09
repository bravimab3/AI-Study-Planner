from app.ingestion.parsers import extract_text_from_pdf
from app.ingestion.chunker import chunk_pages


pdf_path = "/app/uploads/BCSE305L_MODULE-1.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = chunk_pages(pages)

print("Number of pages:", len(pages))
print("Number of chunks:", len(chunks))

for chunk in chunks[:5]:
    print("\n====================")
    print("Page:", chunk["page_number"])
    print("Chunk:", chunk["chunk_index"])
    print(chunk["text"][:300])