from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_service import GeminiService
from fastapi import UploadFile, File
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from services.ingest_service import IngestService
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
app = FastAPI(title="Astralis API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/papers",
    StaticFiles(directory="data/papers"),
    name="papers"
)
# Create service instance
gemini_service = GeminiService()
ingest_service = IngestService()

# -------------------
# Schemas
# -------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


# -------------------
# Routes
# -------------------
@app.get("/")
def root():
    return {"message": "Welcome to Astralis 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        response = gemini_service.chat(
            request.session_id,
            request.message
        )

        return ChatResponse(response=response)


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    upload_dir = Path("data/papers")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store in vector database
    result = ingest_service.ingest(str(file_path))

    # Read PDF
    reader = PdfReader(str(file_path))

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    # Limit text so Gemini doesn't exceed token limits
    text = text[:20000]

    prompt = f"""
You are an astronomy research assistant.

Summarize this research paper.

Format:

Title

Overview

Key Contributions
• Bullet
• Bullet

Methodology
• Bullet

Main Findings
• Bullet

Conclusion

Paper:

{text}
"""

    response = gemini_service.generate_with_retry(prompt)

    return {

        "message": "Paper uploaded successfully.",

        "paper": result["paper"],

        "chunks": result["chunks"],

        "summary": response.text

    }