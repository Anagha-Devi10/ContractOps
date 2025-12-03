import re
from app.schemas import ContractOut


def answer_question_over_contracts(question: str, contracts, memory):
    q = question.lower()

    # 1. The UI always sends 1 selected contract → use it first
    # (contracts list always contains all contracts, but frontend knows the selected one)
    # So, we pick the LAST CONTRACT in the list = selected one
    target: ContractOut = contracts[-1]

    # ---- Structured QA ----
    if "expire" in q or "expiry" in q or "end" in q:
        if target.expiry_date:
            return f"This contract expires on {target.expiry_date}"
        else:
            return "The expiry date is not specified in this contract."

    if "effective" in q or "start date" in q:
        if target.effective_date:
            return f"The effective date is {target.effective_date}"
        else:
            return "The effective date is not available."

    if "payment" in q:
        if target.payment_terms:
            return f"Payment terms: {target.payment_terms}"
        else:
            return "Payment terms are not mentioned."

    if "parties" in q or "who are" in q:
        if target.parties:
            return f"The parties are: {target.parties}"
        else:
            return "Parties could not be extracted."

    # ---- Memory fallback ----
    result = memory.query(question, top_k=1)
    if result:
        r = result[0]
        return (
            f"I couldn't answer directly. Best match is contract {r['contract_id']} "
            f"(score {r['score']:.2f})."
        )

    return "I’m not sure how to answer that."
