import fitz, pytesseract
from PIL import Image
import io

def extract_text_and_chunks(filepath, chunk_size=1000, overlap=200):
    doc = fitz.open(filepath)
    text_content = ""
    for page_index in range(len(doc)):
        page = doc[page_index]
    
        text = page.get_text("text")
        
        
        if not text.strip():  
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text
        text_content += text + "\n"

    chunks = [text_content[i:i+chunk_size] for i in range(0, len(text_content), chunk_size - overlap)]
    return chunks
