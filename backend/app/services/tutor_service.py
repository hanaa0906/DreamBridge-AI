"""Module 7: AI Tutor — retrieval-augmented chat grounded in a lesson.

Chunks the lesson text, embeds chunks with sentence-transformers, retrieves
the most relevant chunks for a student's question with FAISS, then asks the
LLM to answer using only those chunks. Falls back to naive keyword matching
if the embedding model isn't available (e.g. offline / no internet on first
run to download the model), so the endpoint never hard-fails.
"""
import re
from typing import List, Tuple

from app.services import llm_service

_embedder = None
_index_cache = {}  # lesson_id -> (faiss index, chunks)


def _chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks or [text]


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


def _build_index(lesson_id: int, text: str):
    import faiss
    import numpy as np

    chunks = _chunk_text(text)
    embedder = _get_embedder()
    vectors = embedder.encode(chunks, convert_to_numpy=True)
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors.astype(np.float32))
    _index_cache[lesson_id] = (index, chunks)
    return index, chunks


def _retrieve(lesson_id: int, text: str, query: str, k: int = 3) -> List[str]:
    try:
        import numpy as np

        if lesson_id in _index_cache:
            index, chunks = _index_cache[lesson_id]
        else:
            index, chunks = _build_index(lesson_id, text)

        embedder = _get_embedder()
        q_vec = embedder.encode([query], convert_to_numpy=True).astype(np.float32)
        _, indices = index.search(q_vec, min(k, len(chunks)))
        return [chunks[i] for i in indices[0] if i < len(chunks)]
    except Exception:
        # Fallback: naive keyword overlap scoring, no ML deps required
        chunks = _chunk_text(text)
        query_words = set(re.findall(r"\w+", query.lower()))
        scored: List[Tuple[int, str]] = []
        for c in chunks:
            c_words = set(re.findall(r"\w+", c.lower()))
            scored.append((len(query_words & c_words), c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:k]] or chunks[:k]


def answer(lesson_id: int, lesson_text: str, question: str) -> str:
    context_chunks = _retrieve(lesson_id, lesson_text, question)
    context = "\n\n---\n\n".join(context_chunks)

    fallback = (
        "Here's what the lesson says that's most related to your question:\n\n"
        f"{context[:800]}"
    )
    prompt = (
        "You are a patient, encouraging AI tutor. Answer the student's question "
        "using ONLY the lesson excerpts below. If the excerpts don't contain the "
        "answer, say so honestly and suggest what part of the lesson to re-read.\n\n"
        f"LESSON EXCERPTS:\n{context}\n\n"
        f"STUDENT QUESTION: {question}"
    )
    return llm_service.generate(prompt, fallback)
