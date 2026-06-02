from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

pdf_chunks = []
pdf_embeddings = []


def chunk_text(text, chunk_size=300, overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def store_pdf_chunks(text):

    global pdf_chunks
    global pdf_embeddings

    pdf_chunks = chunk_text(text)

    print("\n========================")
    print("RAG DEBUG")
    print("========================")
    print("Total Chunks:", len(pdf_chunks))
    print("========================\n")

    pdf_embeddings = model.encode(pdf_chunks)


def retrieve_relevant_chunks(question, top_k=5):

    global pdf_chunks
    global pdf_embeddings

    if len(pdf_chunks) == 0:
        return ""

    question_embedding = model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        pdf_embeddings
    )[0]

    top_indices = np.argsort(similarities)[-top_k:]

    relevant_chunks = []

    print("\n========================")
    print("QUESTION DEBUG")
    print("========================")
    print(question)
    print("========================\n")

    print("TOP MATCHES\n")

    for idx in reversed(top_indices):

        print(
            f"Score: {similarities[idx]:.4f}"
        )

        print(
            pdf_chunks[idx][:200]
        )

        print(
            "\n------------------\n"
        )

        relevant_chunks.append(
            pdf_chunks[idx]
        )

    return "\n\n".join(relevant_chunks)