# Fast Api app

from fastapi import FastAPI 
from backend.schemas import SummarizeRequest, SummarizeResponse
from utils.chunker import chunk_text
from utils.llm import summarize_chunks

app = FastAPI(title="Contract Risk Analyzer API")

from fastapi import FastAPI

from backend.schemas import (
    SummarizeRequest,
    SummarizeResponse,
    RiskAnalysisRequest,
    RiskAnalysisResponse,
)

from utils.chunker import chunk_text
from utils.llm import summarize_chunks, analyze_risks_for_chunks

@app.post("/summarize", response_model=
SummarizeResponse)
def summarize_contract_api(request: SummarizeRequest):
    chunks = chunk_text(request.text)
    summary = summarize_chunks(chunks)
    return {"summary": summary}

@app.post("/risk-analysis", response_model=RiskAnalysisResponse)
def risk_analysis_api(request: RiskAnalysisRequest):
    chunks = chunk_text(request.text)
    risks = analyze_risks_for_chunks(chunks)
    return risks
