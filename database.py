import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "rag.db"


def create_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            chunk_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL,
            token_count INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_chunks(chunks):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM chunks")

    for chunk in chunks:
        source = chunk["source"]
        title = source.rsplit(".", 1)[0]
        content = chunk["content"]
        token_count = len(content.split())
        embedding_text = ",".join(map(str, chunk["embedding"]))

        cursor.execute(
            """
            INSERT INTO chunks (
                source,
                title,
                chunk_id,
                content,
                embedding,
                token_count
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                source,
                title,
                chunk["chunk_id"],
                content,
                embedding_text,
                token_count,
            ),
        )

    connection.commit()
    connection.close()

def load_chunks():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            source,
            title,
            chunk_id,
            content,
            embedding,
            token_count
        FROM chunks
    """)

    rows = cursor.fetchall()

    connection.close()

    chunks = []

    for row in rows:
        embedding = [
            float(value)
            for value in row[5].split(",")
        ]

        chunks.append({
            "id": row[0],
            "source": row[1],
            "title": row[2],
            "chunk_id": row[3],
            "content": row[4],
            "embedding": embedding,
            "token_count": row[6]
        })

    return chunks
