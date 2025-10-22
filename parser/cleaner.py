import re
from datetime import datetime

def clean_currency(value):
    if not value:
        return None
    value = str(value).replace(",", "")
    value = re.sub(r"(Rs\.?|INR|\$)", "", value, flags=re.I).strip()
    match = re.search(r"[-+]?\d*\.\d+|\d+", value)
    return float(match.group()) if match else None

def clean_date(value):
    """
    Cleans date-like strings to DD/MM/YYYY or returns text like 'Immediate' if no date exists.
    Handles variations such as 'Payment Due Date : Immediate', 'Due Immediately', etc.
    """
    if not value:
        return None

    val_str = str(value).strip()
    val_str = val_str.replace(":", " ").replace("-", " ").replace("_", " ")
    val_str = " ".join(val_str.split())  # normalize spaces

    # ✅ Handle all forms of Immediate payments
    if re.search(r"(immediate|due\s+immediately|pay\s+immediately|immediate\s+payment)", val_str, flags=re.I):
        return "Immediate"

    # ✅ Common date pattern DD/MM/YYYY or DD-MM-YYYY
    match = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", val_str)
    if match:
        d, m, y = match.groups()
        y = "20" + y if len(y) == 2 else y
        try:
            return datetime(int(y), int(m), int(d)).strftime("%d/%m/%Y")
        except Exception:
            pass

    # ✅ Catch fallback words like "On Receipt", "Upon Statement Generation"
    if re.search(r"(on\s+receipt|upon\s+statement|asap|immediately)", val_str, flags=re.I):
        return "Immediate"

    return None



def clean_output_data(data):
    if not isinstance(data, dict):
        return {}

    # Clean numeric fields
    for field in ["total_due", "min_due", "available_credit"]:
        data[field] = clean_currency(data.get(field))

    # Clean date fields
    for date_field in ["payment_due_date", "statement_date"]:
        data[date_field] = clean_date(data.get(date_field))

    # ✅ If payment_due_date is missing after cleaning, assume 'Immediate'
    if not data.get("payment_due_date"):
        data["payment_due_date"] = "Immediate"

    return data
