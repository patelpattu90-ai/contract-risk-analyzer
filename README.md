📄 AI Contract Risk Analyzer

An end-to-end AI system that analyzes legal contracts to identify risks, score severity, and generate decision-ready summaries by combining LLM-based language understanding with deterministic rule-based reasoning.
Built with a strong focus on explainability, auditability, and real-world legal workflows — not just raw model output.

🚀 What This Project Does

Given a contract PDF, the system:

Extracts and normalizes text from the document
Chunks the text safely to preserve context
Uses an LLM to understand contractual language
Detects potential financial, legal, termination, and ambiguous risks
Applies rule-based logic to score severity

Aggregates results into:
An overall risk score (0–100)
A clear executive summary
A category-wise breakdown of risks with explanations
The goal is to move from “the model says so” → “here’s why this clause is risky”.

🧠 Key Design Principle

LLM for understanding, rules for decisions.
LLMs are used to identify and interpret clauses
Deterministic rules are used to score, rank, and justify risk
This separation makes the system:
More explainable
More auditable
Safer for legal and compliance use cases

🏗️ High-Level Architecture

User Flow

PDF Upload
   ↓
Text Extraction & Cleaning
   ↓
Context-Safe Chunking
   ↓
LLM-Based Clause Understanding
   ↓
Rule-Based Risk Classification & Severity Scoring
   ↓
Risk Aggregation & Sorting
   ↓
Executive Summary + Risk Score + Detailed Breakdown

Tech Stack

Frontend: Streamlit
Backend: FastAPI
LLM: HuggingFace Transformers (FLAN-T5)
Architecture: Modular (LLM logic, rules, API, UI separated)

📊 Outputs
1. Contract Risk Score
Numeric score (0–100)
Risk band: Low / Medium / High
Designed for fast executive decision-making

2. Executive Summary

Plain-English explanation of overall contract risk
Highlights presence of high-risk clauses
Action-oriented (e.g., “Immediate review recommended”)

3. Identified Risks

Each risk includes:
Risk description
Severity (High / Medium / Low)
Reason for severity (rule-based)

Example:

Financial Risk: Late payment penalties
Severity: High
Reason: High impact or one-sided contractual risk
📁 Project Structure
contract-risk-analyzer/
├── app.py                 # Streamlit frontend
├── backend/
│   └── main.py            # FastAPI endpoints
├── utils/
│   ├── pdf_loader.py      # PDF text extraction
│   ├── chunker.py         # Safe text chunking
│   └── llm.py             # LLM + rule-based logic
├── requirements.txt
└── README.md
⚙️ How to Run Locally
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Start backend (FastAPI)
uvicorn backend.main:app --reload
3️⃣ Start frontend (Streamlit)
streamlit run app.py

🧪 Example Use Cases

-Contract review for startups & SMEs
-Vendor agreement risk screening
-Legal/compliance pre-checks
-AI system design interviews (LLM + rules architecture)

⚠️ Known Limitations (Intentional & Explicit)

Uses a general-purpose LLM, not a fine-tuned legal model
Cross-clause reasoning (interactions between distant clauses) is limited
Risk score is heuristic, not legally calibrated

These are conscious tradeoffs to keep the system:
Interpretable
Modular
Easy to evolve

🔮 Planned Improvements

Clause-level explainability (“this clause triggered Rule X”)
Highlighting risky clauses directly in text
Cross-chunk reasoning for interacting clauses
Domain-specific legal model fine-tuning

🧑‍💻 Why This Project Matters

Most GenAI demos stop at “LLM generated output.”
This project focuses on system design, risk reasoning, and decision quality — the things that actually matter in production AI systems.

