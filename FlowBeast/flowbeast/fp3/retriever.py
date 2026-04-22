from .embedding import embed_text
from .store import FP3Store

class FP3Retriever:
    def __init__(self):
        self.store = FP3Store()

    def retrieve(self, query: str, k=2):
        vec = embed_text(query)
        return self.store.search(vec, k)
