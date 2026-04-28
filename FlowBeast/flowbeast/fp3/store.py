import faiss
import numpy as np
import json
from pathlib import Path
from flowbeast.core.config import settings

class FP3Store:
    def __init__(self, dim=1536):
        # 确保路径是 Path 对象
        self.index_path = settings.FP3_INDEX_PATH
        self.meta_path = settings.FP3_META_PATH
        
        self.index = faiss.IndexFlatL2(dim)
        self.meta = []

        # 确保目录存在
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        if self.index_path.exists():
            self.load()

    # 用于管理FP3相关元数据和高维向量的存储（基于FAISS），支持向量添加、相似查询、保存与加载。
    def add(self, vectors, items: list):
        self.index.add(np.array(vectors).astype("float32"))
        self.meta.extend(items)

    # The following methods provide basic capabilities for adding vectors (with metadata) to the FAISS index,
    # searching for the k nearest vectors, and saving/loading both the index and the metadata to disk.
    def search(self, vector, k=2):
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(np.array([vector]).astype("float32"), k)
        # 过滤掉无效索引 (-1)
        return [self.meta[i] for i in I[0] if i != -1 and i < len(self.meta)]
    
    # This class implements a simple FAISS-based vector store for FP3, supporting addition, search, saving, and loading of vectors along with their associated metadata.
    def save(self):
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)
    
    # 保存索引和元信息到磁盘
    def load(self):
        self.index = faiss.read_index(str(self.index_path))
        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.meta = json.load(f)
