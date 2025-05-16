# app/main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.resume_parser import extract_text_from_pdf, extract_entities
from app.scoring import get_similarity_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later use frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(resume: UploadFile, job_description: str = Form(...)):
    # Save and read PDF text
    with open(resume.filename, "wb") as f:
        f.write(await resume.read())
    text = extract_text_from_pdf(resume.filename)

    # Extract entities and calculate similarity
    entities = extract_entities(text)
    score = get_similarity_score(text, job_description)

    return {
        "extracted_entities": entities,
        "similarity_score": round(score, 2)
    }
