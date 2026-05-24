"""
FP3 Retriever: RAG retrieval interface for the drama generation pipeline.

Role: Embeds a query topic, searches the FAISS index, returns top-k ranked
ViralUnit/ViralScript examples as dicts. Called inside generator.py
before the LLM prompt is assembled.

This is the read path of the FP3 knowledge base.
"""

from .embedding import embed_text
from .store import FP3Store


class FP3Retriever:
    def __init__(self):
        self.store = FP3Store()

    def retrieve(self, query: str, k=2):
        vec = embed_text(query)
        return self.store.search(vec, k)
