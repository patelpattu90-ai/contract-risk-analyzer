import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from utils.llm import summarize_contract, summarize_chunks
from utils.chunker import chunk_text
from backend.schemas import RiskAnalysisRequest, RiskAnalysisResponse
from utils.llm import analyze_risks_for_chunks
import requests

st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")

st.title("📄 AI Contract Risk Analyzer")

uploaded_file = st.file_uploader("Upload a contract PDF", type=["pdf"])
st.info("⏳ Processing may take 30–60 seconds for large documents")

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
        try:
            response = requests.post(
                "http://127.0.0.1:8000/summarize",
                json={"text": document_text},
                timeout=60  # ⬅️ IMPORTANT
            )

            response.raise_for_status()
            summary = response.json()["summary"]

            st.subheader("🧠 AI Summary (via FastAPI)")
            st.write(summary)

        except requests.exceptions.Timeout:
            st.error("⏱️ Backend is taking too long. Try a smaller document.")

        except Exception as e:
            st.error(f"❌ Backend error: {e}")