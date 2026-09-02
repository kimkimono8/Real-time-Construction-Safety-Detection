from typing import List
from pydantic import BaseModel

class DetectionDetail(BaseModel):
    label: str
    confidence: float

class ComplianceResponse(BaseModel):
    status: str
    total_detected: int
    detected_items: List[str]
    message: str
