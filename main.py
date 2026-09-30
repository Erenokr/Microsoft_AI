from document_loader import load_documents
from chunker import chunk_documents
from embedding_manager import EmbeddingManager
from database import create_database, save_chunks, load_chunks
from retriever import retrieve_top_chunks



def main():
    embedding_manager = None

    # Sistemi hazırla
    create_database()

    documents = load_documents()
    if not documents:
        raise RuntimeError("documents klasöründe okunabilir bir .txt dosyası bulunamadı.")

    chunks = chunk_documents(documents)

    embedding_manager = EmbeddingManager()

    chunks = embedding_manager.generate_embeddings(chunks)
    save_chunks(chunks)

    stored_chunks = load_chunks()

    credits = 100
    print("\n========================================")
    print("        EREN LOCAL RAG ASSISTANT")
    print("========================================")
    print("Sistem hazır.")
    print("Çıkmak için 'exit' yaz.\n")

    print("Hoş geldin! Ben Eren Asistan. Sorularınızı bana sorabilirsiniz.\n")

    try:
        while True:
            question = input("You > ").strip()

            if question.lower() == "exit":
                print("\nAI > Görüşürüz 👋")
                break

            if not question:
                continue

            credits -= 1
            print(f"DEBUG - Credits: {credits}")

            # Kullanıcının sorusunu embedding'e çevir
            question_embedding = embedding_manager.generate_embedding(question)

            # En alakalı metin parçasını bul.
            results = retrieve_top_chunks(
                question_embedding,
                stored_chunks,
                top_k=1,
                question=question,
            )

            # TXT metnini değiştirmeden göster; cevap modeli kullanma.
            answer = (
                results[0]["chunk"]["content"]
                if results else "Bu konu hakkında bir bilgim yok"
            )

            print(f"\nAI > {answer}\n")

    finally:
        # Program kapanırken arama modelini bellekten çıkar.
        if embedding_manager is not None:
            embedding_manager.unload()


if __name__ == "__main__":
    main()
