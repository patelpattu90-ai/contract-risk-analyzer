from fastapi import FastAPI
from backend.schemas import (
    SummarizeRequest,
    SummarizeResponse,
    RiskAnalysisRequest,
)
from utils.chunker import chunk_text
from utils.llm import (
    summarize_chunks,
    analyze_risks_for_chunks,
    enrich_risks_with_severity,
    sort_risks_by_severity,
    generate_executive_summary,
)

app = FastAPI(title="Contract Risk Analyzer API")


# =========================
# Summary Endpoint (Day 3)
# =========================
@app.post("/summarize", response_model=SummarizeResponse)
def summarize_contract_api(request: SummarizeRequest):
    chunks = chunk_text(request.text)
    summary = summarize_chunks(chunks)

    return {
        "summary": summary
    }


# =========================
# Risk Analysis Endpoint (Day 6)
# =========================
@app.post("/risk-analysis")
def risk_analysis_api(request: RiskAnalysisRequest):
    chunks = chunk_text(request.text)

    # 1. Extract risks
    risks = analyze_risks_for_chunks(chunks)

    # 2. Enrich with severity
    enriched = enrich_risks_with_severity(risks)

    # 3. Sort by severity
    sorted_risks = sort_risks_by_severity(enriched)

    # 4. Calculate risk score
    risk_score = calculate_contract_risk_score(sorted_risks)

    # 5. Generate executive summary
    executive_summary = generate_executive_summary(sorted_risks)

    return {
        "executive_summary": executive_summary,
        "risk_score": risk_score,
        "risks": sorted_risks
    }
    
def calculate_contract_risk_score(enriched_risks: dict) -> dict:
    score = 0
    breakdown = []

    severity_weights = {
        "High": 30,
        "Medium": 15,
        "Low": 5
    }

    for category, items in enriched_risks.items():
        for item in items:
            severity = item.get("severity", "Low")
            weight = severity_weights.get(severity, 0)
            score += weight

            breakdown.append({
                "risk": item["risk"],
                "severity": severity,
                "weight": weight
            })

    score = min(score, 100)

    if score <= 20:
        label = "Low Risk"
    elif score <= 50:
        label = "Medium Risk"
    else:
        label = "High Risk"

    return {
        "score": score,
        "label": label,
        "breakdown": breakdown
    }