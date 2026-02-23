def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100
):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

        if start < 0:
            start = 0

    return chunks
    print("🧩 chunk_text called, text length:", len(text))