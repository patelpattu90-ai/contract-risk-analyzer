# Request - response models
from pydantic import BaseModel
from typing import List, Dict


# ========= Day 3 =========

class SummarizeRequest(BaseModel):
    text: str


class SummarizeResponse(BaseModel):
    summary: str


# ========= Day 4 =========

class RiskAnalysisRequest(BaseModel):
    text: str


class RiskItem(BaseModel):
    risk: str
    severity: str
    reason: str


class RiskAnalysisResponse(BaseModel):
    financial_risks: List[RiskItem]
    legal_risks: List[RiskItem]
    termination_risks: List[RiskItem]
    ambiguous_clauses: List[RiskItem]