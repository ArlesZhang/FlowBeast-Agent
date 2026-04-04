import faiss
import numpy as np
import json
from flowbeast.core.config import settings
from pathlib import Path

class FP3Store:
    def __init__(self, dim=1536):
        # 显式转换为 Path 对象
        self.index_path = Path(settings.FP3_INDEX_PATH)
        self.meta_path = Path(settings.FP3_META_PATH)
        
        self.index = faiss.IndexFlatL2(dim)
        self.meta = []
        
        if self.index_path.exists():
            self.load()

    def add(self, vector, item_dict):
        self.index.add(np.array([vector]).astype("float32"))
        self.meta.append(item_dict)

    def search_with_scores(self, vector, k=5):
        if self.index.ntotal == 0: return [], [], []
        D, I = self.index.search(np.array([vector]).astype("float32"), k)
        metas = [self.meta[i] for i in I[0] if i < len(self.meta) and i != -1]
        return D[0], I[0], metas

    def save(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def load(self):
        self.index = faiss.read_index(str(self.index_path))
        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.meta = json.load(f)
