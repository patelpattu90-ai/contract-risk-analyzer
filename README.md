 AI Contract Risk Analyzer

An end-to-end **AI-powered contract analysis system** that summarizes legal contracts and identifies key risks using **FastAPI**, **LLMs**, and **Streamlit**.

This project follows a **backend-first architecture**, with clear API boundaries, chunk-based LLM processing, and a lightweight frontend for demonstration.
 Features

✅ Contract Summarization
- Upload a contract (PDF or text)
- Text is chunked to fit LLM context limits
- Each chunk is summarized independently
- Summaries are combined into a final contract summary

 ✅ Contract Risk Analysis
- Dedicated `/risk-analysis` API endpoint
- Identifies and categorizes:
  - Financial risks
  - Legal risks
  - Termination risks
  - Ambiguous clauses
- Chunk-level risk extraction
- Aggregated and structured JSON response
- Rule-based fallback for robustness when LLM output is weak

 ✅ Backend-First Design
- FastAPI REST APIs
- Swagger (OpenAPI) testing
- Clean request/response schemas using Pydantic
- Frontend consumes backend via HTTP



 System Architecture


PDF / Text
↓
Text Extraction
↓
Chunking (context-window safe)
↓
LLM Processing
├─ Summarization
└─ Risk Analysis
↓
Aggregation + Fallback Logic
↓
FastAPI JSON Response
↓
Streamlit UI


---

 Tech Stack

- **Backend**: FastAPI, Pydantic
- **Frontend**: Streamlit
- **LLM**: Hugging Face Transformers (`distilgpt2`)
- **PDF Parsing**: Custom text extraction utility
- **Language**: Python 3.10+
- **API Testing**: Swagger UI


 Project Structure


contract-risk-analyzer/
│
├── backend/
│ ├── main.py # FastAPI app & routes
│ ├── schemas.py # Request/Response models
│
├── utils/
│ ├── llm.py # LLM prompts, parsing, aggregation
│ ├── chunker.py # Text chunking logic
│ ├── pdf_loader.py # PDF text extraction
│
├── app.py # Streamlit UI
├── requirements.txt
├── README.md
