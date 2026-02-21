import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from utils.llm import summarize_contract, summarize_chunks
from utils.chunker import chunk_text
import requests

st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")

st.title("📄 AI Contract Risk Analyzer")

uploaded_file = st.file_uploader("Upload a contract PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        document_text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(document_text)

    st.subheader("📦 Chunking Info")
    st.write(f"Total chunks created: {len(chunks)}")

    st.write("Preview of first chunk:")
    st.text_area(
    label="",
    value=chunks[0][:1000],
    height=200
)

    st.subheader("Extracted Text (Preview)")
    st.text_area("", document_text[:3000], height=250)

if st.button("Generate Contract Summary"):
    with st.spinner("Sending document to backend..."):
        response = requests.post(
            "http://127.0.0.1:8000/summarize",
            json={"text": document_text}
        )
        summary = response.json()["summary"]

    st.subheader("🧠 AI Summary (via FastAPI)")
    st.write(summary)