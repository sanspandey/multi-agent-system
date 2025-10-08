import os
import uuid
import time
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


load_dotenv()

app = FastAPI(title="Multi-Agent Controller API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


logs = []
file_map = {}  

controller = None


def get_controller():
    
    if not controller:
        from app.agent.pdf_rag import PDFRAGAgent
        from app.agent.controller import Controller

        pdf_agent = PDFRAGAgent()
        ctrl = Controller()
        ctrl.pdf_agent = pdf_agent
        controller = ctrl
    return controller


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        MAX_BYTES = 10 * 1024 * 1024  # 10MB
        data = await file.read()
        if len(data) > MAX_BYTES:
            return JSONResponse({"error": "File too large (max 10MB)"}, status_code=400)

        
        fid = f"{int(time.time())}_{uuid.uuid4().hex}_{file.filename}"
        path = UPLOAD_DIR / fid
        with open(path, "wb") as f:
            f.write(data)

        file_map[fid] = file.filename

        print(f"DEBUG >>> ingesting {path} as {fid}")
        ctrl = get_controller()
        ingest_result = ctrl.pdf_agent.ingest_pdf(str(path), fid)
        print(f"DEBUG >>> Ingest result: {ingest_result}")

        logs.append({"event": "upload_pdf", "file_id": fid, "filename": file.filename})
        return {"status": "uploaded", "file_id": fid, "ingested": ingest_result}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/ask")
async def ask(query: str = Form(...), file_ids: str = Form(None)):
    try:
        fid = file_ids.split(",")[0] if file_ids else None
        filename = file_map.get(fid) if fid else None

        print(f"DEBUG >>> Received query: {query}")
        print(f"DEBUG >>> Using file_id: {fid}")

        ctrl = get_controller()
        result = ctrl.handle_query(query, fid, filename)

        logs.append({"event": "ask", "query": query, "result": result})
        return JSONResponse(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/logs")
def get_logs():

    return logs[-50:]
