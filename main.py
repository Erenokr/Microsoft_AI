from document_loader import load_documents
from chunker import chunk_documents
from embedding_manager import EmbeddingManager
from database import create_database, save_chunks, load_chunks
from retriever import retrieve_top_chunks
from promptBuilder import build_prompt
from chatBot import Chatbot



def main():
    embedding_manager = None
    chatbot = None

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

    chatbot = Chatbot()
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

            # En alakalı 3 chunk'ı bul
            results = retrieve_top_chunks(
                question_embedding,
                stored_chunks,
                top_k=3
            )

            # RAG prompt'unu oluştur
            prompt = build_prompt(question, results)

            # LLM cevabını üret
            answer = chatbot.generate_answer(prompt)

            print(f"\nAI > {answer}\n")

    finally:
        # Program kapanırken modelleri bellekten çıkar
        if chatbot is not None:
            chatbot.unload()
        if embedding_manager is not None:
            embedding_manager.unload()


if __name__ == "__main__":
    main()
