# Request - response models

from pydantic import BaseModel
from typing import List

# Validates incoming req
class SummarizeRequest(BaseModel):
    text: str

# Validates incoming response
class SummarizeResponse(BaseModel):
    summary: str