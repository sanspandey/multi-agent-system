import fitz  # PyMuPDF

def extract_text_and_chunks(filepath, chunk_size=1000, overlap=200):
    
    doc = fitz.open(filepath)
    text_content = ""
    for page in doc:
        text = page.get_text("text")
        text_content += text + "\n"

    # Split into overlapping chunks
    chunks = [
        text_content[i:i + chunk_size]
        for i in range(0, len(text_content), chunk_size - overlap)
    ]
    return chunks
