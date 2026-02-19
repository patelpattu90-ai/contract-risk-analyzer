import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from utils.llm import summarize_contract

st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")

st.title("📄 AI Contract Risk Analyzer")

uploaded_file = st.file_uploader("Upload a contract PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        document_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Text (Preview)")
    st.text_area("", document_text[:3000], height=250)

    if st.button("Generate Contract Summary"):
        with st.spinner("Analyzing contract using LLM..."):
            summary = summarize_contract(document_text)

        st.subheader("🧠 AI Summary")
        st.write(summary)
