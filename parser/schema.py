def normalize_and_validate(data):
    if not isinstance(data, dict):
        return {}
    return {
        "issuer": data.get("issuer"),
        "card_last_4": str(data.get("card_last_4", "")).strip()[-4:] or None,
        "billing_period": data.get("billing_period"),
        "payment_due_date": data.get("payment_due_date"),
        "statement_date": data.get("statement_date"),
        "total_due": data.get("total_due"),
        "min_due": data.get("min_due"),
        "available_credit": data.get("available_credit"),
    }
