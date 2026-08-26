from foundry_local_sdk import Configuration, FoundryLocalManager


class EmbeddingManager:
    def __init__(self):
        # Foundry Local'i başlat
        config = Configuration(app_name="erenAsisstant")
        FoundryLocalManager.initialize(config)

        self.manager = FoundryLocalManager.instance

        # Embedding modelini katalogdan al
        self.model = self.manager.catalog.get_model(
            "qwen3-embedding-0.6b"
        )

        # Model bilgisayarda yoksa indir
        self.model.download(
            lambda progress: print(
                f"\rEmbedding modeli indiriliyor: {progress:.1f}%",
                end="",
                flush=True
            )
        )

        print()

        # Modeli belleğe yükle
        self.model.load()

        # Embedding işlemleri için client oluştur
        self.client = self.model.get_embedding_client()

    def generate_embedding(self, text):
        """
        Tek bir metni embedding'e çevirir.
        Örneğin kullanıcının sorusu.
        """
        response = self.client.generate_embeddings([text])

        return response.data[0].embedding

    def generate_embeddings(self, chunks):
        """
        Birden fazla chunk için embedding oluşturur.
        """

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        response = self.client.generate_embeddings(texts)

        for chunk, item in zip(chunks, response.data):
            chunk["embedding"] = item.embedding

        return chunks

    def unload(self):
        """
        İşimiz bittiğinde embedding modelini bellekten çıkarır.
        """
        self.model.unload()