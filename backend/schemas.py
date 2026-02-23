# Request - response models
from pydantic import BaseModel
from typing import List


# ========= Day 3 =========

class SummarizeRequest(BaseModel):
    text: str


class SummarizeResponse(BaseModel):
    summary: str


# ========= Day 4 =========

class RiskAnalysisRequest(BaseModel):
    text: str


class RiskAnalysisResponse(BaseModel):
    financial_risks: List[str]
    legal_risks: List[str]
    termination_risks: List[str]
    ambiguous_clauses: List[str]