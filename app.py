import streamlit as st
import requests

from utils.pdf_loader import extract_text_from_pdf
from utils.chunker import chunk_text

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")
st.title("📄 AI Contract Risk Analyzer")
st.info("⏳ Processing may take 30–60 seconds for large documents")

# -----------------------------
# File upload
# -----------------------------
uploaded_file = st.file_uploader("Upload a contract PDF", type=["pdf"])

document_text = None
chunks = []

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        document_text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(document_text)

    st.subheader("📦 Chunking Info")
    st.write(f"Total chunks created: {len(chunks)}")

    st.subheader("📄 Extracted Text (Preview)")
    st.text_area(
        label="Extracted text",
        value=document_text[:3000],
        height=250,
        label_visibility="collapsed"
    )

# -----------------------------
# Contract Summary
# -----------------------------
if document_text and st.button("🧠 Generate Contract Summary"):
    with st.spinner("Sending document to backend for summary..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/summarize",
                json={"text": document_text[:3000]},
                timeout=60
            )
            response.raise_for_status()
            summary = response.json()["summary"]

            st.subheader("🧠 AI Summary")
            st.write(summary)

        except Exception as e:
            st.error(f"❌ Backend error: {e}")

# -----------------------------
# Risk Analysis
# -----------------------------
st.divider()
st.subheader("⚠️ Contract Risk Analysis")

def severity_icon(severity: str) -> str:
    if severity == "High":
        return "🔴"
    if severity == "Medium":
        return "🟠"
    return "🟢"

if document_text and st.button("🚨 Analyze Contract Risks"):
    with st.spinner("Analyzing contract risks..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/risk-analysis",
                json={"text": document_text[:3000]},
                timeout=60
            )
            response.raise_for_status()
            risk_data = response.json()

        except Exception as e:
            st.error(f"❌ Backend error: {e}")
            st.stop()

    # -------------------------
    # Contract Risk Score
    # -------------------------
    st.subheader("📊 Contract Risk Score")

    score_data = risk_data["risk_score"]

    st.metric(
        label="Overall Risk Score",
        value=f"{score_data['score']} / 100",
        delta=score_data["label"]
    )

    if score_data["label"] == "High Risk":
        st.error("🚨 High risk contract – immediate review recommended")
    elif score_data["label"] == "Medium Risk":
        st.warning("⚠️ Medium risk contract – review key clauses")
    else:
        st.success("✅ Low risk contract")

    # -------------------------
    # Executive Summary
    # -------------------------
    st.subheader("📌 Executive Summary")
    st.success(risk_data["executive_summary"])

    # -------------------------
    # Risks
    # -------------------------
    st.subheader("⚠️ Identified Risks")

    risks_by_category = risk_data["risks"]

    for category, items in risks_by_category.items():
        if not items:
            continue

        st.markdown(f"### {category.replace('_', ' ').title()}")

        for item in items:
            icon = severity_icon(item["severity"])

            st.markdown(f"{icon} **{item['risk']}**")
            st.write(f"**Severity:** {item['severity']}")
            st.write(f"**Reason:** {item['reason']}")
            st.divider()