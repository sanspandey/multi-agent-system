from app.utils.pdf_utils import extract_text_and_chunks
from app.storage.embedding_storage import EmbeddinsStore

class PDFRAGAgent:
    def __init__(self):
        self.store = EmbeddinsStore()
        
    def ingest_pdf(self, filepath, source_id):
        print(f"DEBUG >>> ingesting {filepath} as {source_id}")
        chunks = extract_text_and_chunks(filepath)
        print(f"DEBUG >>> got {len(chunks)} chunks from {filepath}")
        
        
        for i, chunk in enumerate(chunks):
            self.store.upsert(chunk, {"source": source_id, "chunk": i})
        print(f"DEBUG >>> total chunks in store {len(self.store._db)}")
        
        return {"ingested_chunks": len(chunks)}
    
    def query(self, query, filename):   
        result = self.store.search(query, k=5, filter_source=filename)
        print("DEBUG >>> query asked for:", filename)
        print("DEBUG >>> available sources in store:",
      list({item["metadata"]["source"] for item in self.store._db}))

        return {"snippets": result}
    
