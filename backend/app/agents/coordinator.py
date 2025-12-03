
import uuid
from app.schemas import ContractIn, ContractOut
from app.agents.extractors import extract_all_facts
from app.agents.summarizer import summarize_text
from app.agents.validator import validate_facts
from app.agents.tasks import generate_tasks
from app.utils.memory import MemoryBank
from app.utils.qa import answer_question_over_contracts
from app.utils.logger import logger

_STORE = {}
_MEMORY = MemoryBank()

def get_contract_store():
    return _STORE

def process_contract(payload: ContractIn) -> ContractOut:
    cid = str(uuid.uuid4())[:8]
    logger.info(f"Processing contract {cid}")

    extracted = extract_all_facts(cid, payload.text)
    extracted["summary"] = summarize_text(payload.text)
    validated = validate_facts(extracted)

    contract = ContractOut(
        contract_id=cid,
        title=payload.title,
        parties=validated["parties"],
        effective_date=validated["effective_date"],
        expiry_date=validated["expiry_date"],
        renewal_terms=validated["renewal_terms"],
        payment_terms=validated["payment_terms"],
        obligations=validated["obligations"],
        summary=validated["summary"],
        confidence=validated["confidence"],
    )

    _STORE[cid] = contract
    _MEMORY.add_contract(contract)
    generate_tasks(contract)

    return contract

def answer_question(question: str, contracts):
    return answer_question_over_contracts(question, contracts, _MEMORY)
