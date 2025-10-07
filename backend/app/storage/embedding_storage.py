import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddinsStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._db = []
        
    def upsert(self,text,metadata=None):
        emb = self.model.encode(text)
        rec = {"id":uuid.uuid4().hex, "text":text,"emb":emb,"metadata":metadata or {}}
        self._db.append(rec)
        return rec["id"]
    
    def search(self,query, k=5, filter_source=None):
        q_emb =  self.model.encode(query)
        result = []
        for r in self._db:
            if filter_source and r["metadata"].get("source") != filter_source:
                continue
            score = float(cosine_similarity([q_emb],[r["emb"]])[0][0])
            result.append((score,r))
        result.sort(key=lambda x: -x[0])
        return [{"score":s, "text":r["text"],"metadata":r["metadata"]} for s,r in result[:k]]
    