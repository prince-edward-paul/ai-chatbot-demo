import streamlit as st
import pandas as pd
import google.generativeai as genai
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import io

# -------------------------
# Configure Gemini API
# -------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# -------------------------
# Sidebar (Professional Info)
# -------------------------
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("""
    ### About
    This AI chatbot answers questions using:
    - Knowledge Base CSV FAQs  
    - PDF documents  
    - Website content  
    - Voice input  
    - Context-aware AI responses  

    ### Features
    ✔ FAQ automation  
    ✔ AI responses  
    ✔ Conversation memory  
    ✔ Business-ready chatbot  

    ---
    **Developer**  
    Prince Edward Paul
    """)

# -------------------------
# App Header
# -------------------------
st.title("🤖 AI Chatbot – Gemini Powered (Next-Level)")
st.markdown(
    "Ask a question or select a quick FAQ. Upload PDFs or enter a website URL for enhanced AI responses."
)

# -------------------------
# Chat Memory
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Knowledge Base CSV
# -------------------------
uploaded_csv = st.file_uploader("Upload Knowledge Base CSV", type=["csv"])
if uploaded_csv:
    kb = pd.read_csv(uploaded_csv)
else:
    kb = pd.read_csv("knowledge_base.csv")

# -------------------------
# Category Filter
# -------------------------
categories = kb["Category"].unique().tolist()
selected_category = st.selectbox("Select FAQ Category", ["All"] + categories)

if selected_category != "All":
    filtered_kb = kb[kb["Category"] == selected_category]
else:
    filtered_kb = kb

# -------------------------
# FAQ Buttons
# -------------------------
st.subheader("Quick FAQs")
cols = st.columns(3)
for idx, row in filtered_kb.iterrows():
    col = cols[idx % 3]
    if col.button(row["Question"]):
        st.session_state.history.append(("You", row["Question"]))
        st.session_state.history.append(("Bot", row["Answer"]))

# -------------------------
# PDF Upload Feature
# -------------------------
pdf_text = ""
uploaded_pdf = st.file_uploader("Upload PDF for AI reference", type=["pdf"])
if uploaded_pdf:
    pdf_reader = PdfReader(uploaded_pdf)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() + "\n"

# -------------------------
# Website URL Input
# -------------------------
website_text = ""
website_url = st.text_input("Optional: Enter Website URL for AI reference")
if website_url:
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, "html.parser")
        website_text = soup.get_text(separator="\n")
    except:
        st.warning("Could not fetch website content.")

# -------------------------
# Voice Input (optional)
# -------------------------
voice_input = st.text_input("Optional: Voice Input (type your question if not speaking)")
user_question = st.text_input("Ask your question here")

# -------------------------
# AI Response Function
# -------------------------
def get_ai_response(question):
    # 1. Check Knowledge Base CSV
    kb_match = kb[kb["Question"].str.lower().str.contains(question.lower())]
    if not kb_match.empty:
        return kb_match["Answer"].values[0]

    # 2. Combine context: chat history + PDF + website
    conversation = ""
    for sender, msg in st.session_state.history:
        conversation += f"{sender}: {msg}\n"
    conversation += f"User: {question}\n"

    if pdf_text:
        conversation += f"\n[PDF Reference]:\n{pdf_text}\n"
    if website_text:
        conversation += f"\n[Website Reference]:\n{website_text}\n"

    # Ask Gemini
    response = model.generate_content(conversation)
    return response.text

# -------------------------
# Handle User Input
# -------------------------
if st.button("Send"):
    question = user_question or voice_input
    if question:
        answer = get_ai_response(question)
        st.session_state.history.append(("You", question))
        st.session_state.history.append(("Bot", answer))

# -------------------------
# Display Chat (Styled Bubbles)
# -------------------------
st.markdown("---")
for sender, msg in st.session_state.history:
    if sender == "You":
        st.markdown(
            f"<div style='text-align:right; background-color:#D0E6FF; padding:10px; border-radius:10px; margin:5px;'>"
            f"<b>{sender}:</b> {msg}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background-color:#D4FFD6; padding:10px; border-radius:10px; margin:5px;'>"
            f"<b>{sender}:</b> {msg}</div>",
            unsafe_allow_html=True
        )

# -------------------------
# Professional Footer
# -------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:14px; padding:10px;">
        © 2026 | AI Chatbot | Developed by <b>Prince Edward Paul</b>
    </div>
    """,
    unsafe_allow_html=True
)