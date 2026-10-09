def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[dict]:

    chunks = []

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        start = 0
        chunk_index = 0

        while start < len(text):

            end = start + chunk_size

            # Try to end the chunk at a space
            if end < len(text):
                space_position = text.rfind(" ", start, end)

                if space_position > start:
                    end = space_position

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page_number": page["page_number"],
                    "chunk_index": chunk_index,
                    "text": chunk_text
                })

                chunk_index += 1

            start = end - overlap

    return chunks