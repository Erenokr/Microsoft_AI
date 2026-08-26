from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_PATH = BASE_DIR / "documents"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents
