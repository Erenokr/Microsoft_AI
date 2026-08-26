def chunk_documents(documents, chunk_size=500):
    chunks = []

    for document in documents:
        text = document["content"]
        source = document["source"]

        for i in range(0, len(text), chunk_size):
            chunk_text = text[i:i + chunk_size].strip()

            if not chunk_text:
                continue

            chunks.append({
                "source": source,
                "chunk_id": len(chunks),
                "content": chunk_text
            })

    return chunks
