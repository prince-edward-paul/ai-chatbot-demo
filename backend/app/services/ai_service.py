import requests

from app.services.rag_service import retrieve_relevant_chunks

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "phi3"


def analyze_pdf_text(text):

    prompt = f"""
    Analyze this PDF document and provide:

    1. Summary
    2. Main topics
    3. Important insights
    4. Key points

    PDF Content:

    {text[:1000]}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]


def ask_pdf_question(pdf_text, question):

    relevant_text = retrieve_relevant_chunks(question)

    prompt = f"""
DOCUMENT:
{relevant_text}

QUESTION:
{question}

Instructions:
- Answer ONLY from the DOCUMENT.
- If the answer exists in the DOCUMENT, provide it.
- Do not explain your reasoning.
- Do not say "the context does not provide".
- Keep the answer under 3 sentences.

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        }
    )

    data = response.json()

    return data["response"]