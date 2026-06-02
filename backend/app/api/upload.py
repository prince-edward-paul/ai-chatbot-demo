from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
import io

from app.services.rag_service import store_pdf_chunks
from app.services.ai_service import (
    analyze_pdf_text,
    ask_pdf_question
)

router = APIRouter()

pdf_content = ""


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global pdf_content

    contents = await file.read()

    print("\n========================")
    print("UPLOAD DEBUG")
    print("========================")
    print("Filename:", file.filename)
    print("File Size:", len(contents))
    print("========================\n")

    if len(contents) == 0:
        return {
            "error": "Empty file received by backend"
        }

    pdf = PdfReader(io.BytesIO(contents))

    extracted_text = ""

    for page in pdf.pages:

        text = page.extract_text()

        if text:
            extracted_text += text

    pdf_content = extracted_text

    print("\n========================")
    print("PDF TEXT DEBUG")
    print("========================")
    print("PDF Length:", len(extracted_text))
    print(extracted_text[:500])
    print("========================\n")

    store_pdf_chunks(extracted_text)

    analysis = "PDF uploaded successfully and indexed for questions."

    return {
        "filename": file.filename,
        "analysis": analysis
    }


@router.post("/ask-pdf")
async def ask_pdf(question: dict):

    global pdf_content

    answer = ask_pdf_question(
        pdf_content,
        question["question"]
    )

    return {
        "answer": answer
    }