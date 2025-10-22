# 💳 AI Credit Card Statement Parser (Gemini 2.5 Flash)

A Streamlit app that uses **Google Gemini 2.5 Flash** to extract key fields from any credit card statement PDF.

---

## 🧰 Features

- Works for **multiple issuers** (Axis, IDFC, HDFC, ICICI, SBI, etc.)
- Handles both **text-based and scanned PDFs**
- Extracts:
  - Issuer name
  - Card last 4 digits
  - Billing period
  - Payment due date
  - Total amount due
  - Available credit limit
- Outputs clean **JSON + CSV**
- Uses **Gemini 2.5 Flash API** (free tier)

---

## ⚙️ Setup

```bash
git clone <repo_url>
cd credit-card-parser
pip install -r requirements.txt
