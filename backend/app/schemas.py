
from pydantic import BaseModel
from typing import List, Optional

class Obligation(BaseModel):
    obligation: str
    confidence: float

class ContractIn(BaseModel):
    title: str
    text: str

class ContractOut(BaseModel):
    contract_id: str
    title: str
    parties: Optional[str] = None
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None
    renewal_terms: Optional[str] = None
    payment_terms: Optional[str] = None
    obligations: List[Obligation] = []
    summary: Optional[str] = None
    confidence: float = 1.0

class QARequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    contract_id: str
    question: str
    answer: str
