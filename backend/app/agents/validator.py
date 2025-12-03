
def validate_facts(facts):
    if not facts["effective_date"] or not facts["expiry_date"]:
        facts["confidence"] = 0.8
    return facts
