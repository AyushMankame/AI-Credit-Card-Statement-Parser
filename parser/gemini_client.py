from google import genai
import json
import re
import time
import random

PROMPT = """
You are an expert financial document parser.
From the given credit card statement text, extract only these fields:
- issuer (bank name)
- card_last_4 (last four digits)
- billing_period (DD/MM/YYYY - DD/MM/YYYY)
- payment_due_date (DD/MM/YYYY)
- statement_date (DD/MM/YYYY)
- total_due (numeric, include decimals)
- min_due (minimum payment)
- available_credit (numeric)

Return strictly valid JSON:
{
  "issuer": "",
  "card_last_4": "",
  "billing_period": "",
  "payment_due_date": "",
  "statement_date": "",
  "total_due": "",
  "min_due": "",
  "available_credit": ""
}
"""

class GeminiClient:
    def __init__(self, api_key: str, model="gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def _extract_json(self, text: str) -> dict:
        if not text:
            return {}
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
        return {}

    def _call_with_retry(self, prompt: str, retries: int = 3, delay: float = 2.5):
        for attempt in range(1, retries + 1):
            try:
                resp = self.client.models.generate_content(model=self.model, contents=prompt)
                return resp
            except Exception as e:
                msg = str(e).lower()
                if "503" in msg or "unavailable" in msg:
                    wait = delay * attempt + random.uniform(0, 1.5)
                    print(f"[Retry {attempt}] Model overloaded, retrying in {wait:.1f}s...")
                    time.sleep(wait)
                else:
                    print(f"❌ Gemini API error: {e}")
                    raise
        return None

    def extract_fields(self, statement_text: str) -> dict:
        if not statement_text.strip():
            return {}
        prompt = PROMPT + "\n\n" + statement_text[:8000]
        resp = self._call_with_retry(prompt)
        if not resp:
            return {}
        text = resp.text.strip()
        data = self._extract_json(text)
        return data or {}
