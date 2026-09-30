import math
import re
from difflib import SequenceMatcher
from pathlib import Path


def topic_match(question, source):
    """Kısa tanım sorularında dosya adını ve küçük yazım hatalarını tanı."""
    normalize = lambda text: text.replace("İ", "i").replace("I", "ı").lower()
    words = re.findall(r"[^\W_]+", normalize(question))
    fillers = {"kim", "kimdir", "ne", "nedir", "hakkında", "bilgi", "ver", "bana"}
    topic = [word for word in words if word not in fillers]
    title = normalize(Path(source).stem)
    if len(topic) != 1 or not title:
        return 0
    if topic[0] == title:
        return 2
    if min(len(topic[0]), len(title)) >= 3:
        # Yalnızca tek karakterlik ekleme, silme veya değiştirmeyi kabul et.
        edits = sum(max(i2 - i1, j2 - j1)
                    for tag, i1, i2, j1, j2 in
                    SequenceMatcher(None, topic[0], title).get_opcodes()
                    if tag != "equal")
        if edits == 1:
            return 1
    return 0


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

def retrieve_top_chunks(question_embedding, chunks, top_k=3, min_score=0.5, question=""):
    results = []
    matches = {chunk.get("source", ""): topic_match(question, chunk.get("source", ""))
               for chunk in chunks}
    best_match = max(matches.values(), default=0)
    sources = [source for source, match in matches.items() if match == best_match]
    preferred_source = sources[0] if best_match and len(sources) == 1 else None

    for chunk in chunks:
        score = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        # Bu eşik bir doğruluk olasılığı değil, kosinüs benzerliğidir.
        matched_topic = preferred_source is not None and chunk.get("source") == preferred_source
        if score < min_score and not matched_topic:
            continue

        results.append({
            "score": score,
            "chunk": chunk
        })

    results.sort(
        key=lambda result: (
            preferred_source is not None and result["chunk"].get("source") == preferred_source,
            result["score"],
        ),
        reverse=True
    )

    return results[:top_k]
