import fitz

def extract_text_and_chunks(filepath, chunk_size=1000, overlap=200):
    """
    Extract text from PDF using PyMuPDF and split into overlapping chunks.
    OCR is disabled to save memory on low-RAM servers.
    """
    doc = fitz.open(filepath)
    text_content = ""

    for page in doc:
        text = page.get_text("text")  # extract text only
        text_content += text + "\n"

    # Create overlapping chunks
    chunks = [
        text_content[i:i+chunk_size]
        for i in range(0, len(text_content), chunk_size - overlap)
    ]
    return chunks
