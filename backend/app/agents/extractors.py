
import re
from app.schemas import Obligation
from app.utils.logger import logger

def extract_all_facts(cid: str, text: str):
    logger.info(f"Extracting facts for {cid}")
    return {
        "parties": extract_parties(text),
        "effective_date": extract_effective(text),
        "expiry_date": extract_expiry(text),
        "renewal_terms": extract_renewal(text),
        "payment_terms": extract_payment(text),
        "obligations": extract_obligations(text),
        "summary": None,
        "confidence": 1.0,
    }

def extract_parties(text):
    """
    Try to extract parties from patterns like:
    - 'entered into by Alpha Corp (“Provider”) and Beta Ltd (“Client”) ...'
    - 'entered into by Gamma Solutions ("Provider") and Delta Inc ("Customer") ...'
    - 'between Alpha Corp and Beta Ltd'
    """
    # Pattern 1: entered into by X (role) and Y (role)
    m1 = re.search(
        r"entered into by\s+(.+?)\s*\([^)]+\)\s+and\s+(.+?)\s*\([^)]+\)",
        text,
        flags=re.IGNORECASE,
    )
    if m1:
        p1 = m1.group(1).strip()
        p2 = m1.group(2).strip()
        return f"{p1} and {p2}"

    # Pattern 2: between Alpha Corp and Beta Ltd
    m2 = re.search(
        r"between\s+(.+?)\s+and\s+(.+?)[\.\n]",  # up to dot or newline
        text,
        flags=re.IGNORECASE,
    )
    if m2:
        p1 = m2.group(1).strip()
        p2 = m2.group(2).strip()
        return f"{p1} and {p2}"

    return None

def extract_effective(text):
    m = re.search(r"Effective Date[:\s]*(.+)", text)
    return m.group(1).strip() if m else None

def extract_expiry(text):
    m = re.search(r"until ([A-Za-z]+ \d{1,2}, \d{4})", text)
    return m.group(1) if m else None

def extract_renewal(text):
    m = re.search(r"(Renewal[:].+)", text)
    return m.group(1).strip() if m else None

def extract_payment(text):
    m = re.search(r"(within \d+ days|payable within \d+ days)", text)
    return m.group(1) if m else None

def extract_obligations(text):
    obs = []
    sents = re.split(r"(?<=[.!?])\s+", text)
    for s in sents:
        if re.search(r"\bshall\b|\bmust\b|\bwill\b", s, flags=re.I):
            obs.append(Obligation(obligation=s.strip(), confidence=0.85))
    return obs
