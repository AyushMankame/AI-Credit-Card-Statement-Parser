import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime, timedelta

from parser.pdf_utils import extract_text_from_pdf, extract_text_with_ocr_if_needed
from parser.gemini_client import GeminiClient
from parser.schema import normalize_and_validate
from parser.cleaner import clean_output_data

# ---------------- CONFIG ----------------
GEMINI_API_KEY = "AIzaSyCsIy-ePZi4CrXmWBS6ib95_1lGs9I02zE"
# ----------------------------------------

st.set_page_config(page_title="Credit Card Statement Parser", layout="centered")

st.title("💳 Credit Card Statement Parser")
# st.markdown("""
# Upload up to **5 credit card statements (PDF)**.  
# This system automatically extracts and cleans:
# - Issuer name, last 4 digits  
# - Billing period (inferred if missing)  
# - Statement date, payment due date  
# - Total due, minimum due, available credit  

# ✅ Works even if “Billing Period” text is missing (e.g., HDFC)
# """)

# ----------------------------------------
# Helper function for billing period inference
def infer_billing_period_if_missing(cleaned):
    """If billing period missing but statement_date exists, infer ~30-day window."""
    if not cleaned.get("billing_period") and cleaned.get("statement_date"):
        try:
            stmt = datetime.strptime(cleaned["statement_date"], "%d/%m/%Y")
            start = (stmt - timedelta(days=30)).strftime("%d/%m/%Y")
            end = stmt.strftime("%d/%m/%Y")
            cleaned["billing_period"] = f"{start} - {end}"
        except Exception:
            pass
    return cleaned

# ----------------------------------------
# File uploader
uploaded_files = st.file_uploader(
    "📄 Upload up to 5 Credit Card Statements",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("⚠️ Please upload a maximum of 5 PDFs.")
        st.stop()

    st.info("Processing your PDFs with Gemini 2.5 Flash...")
    client = GeminiClient(GEMINI_API_KEY)
    all_results = []
    progress = st.progress(0)

    total = len(uploaded_files)
    for idx, file in enumerate(uploaded_files, start=1):
        text = extract_text_from_pdf(file)
        if not text.strip():
            text = extract_text_with_ocr_if_needed(file)

        parsed = client.extract_fields(text)

        # Safeguard for None
        if not isinstance(parsed, dict):
            parsed = {}

        normalized = normalize_and_validate(parsed)
        cleaned = clean_output_data(normalized)
        cleaned = infer_billing_period_if_missing(cleaned)
        cleaned["file_name"] = file.name

        all_results.append(cleaned)
        progress.progress(idx / total)

    st.success("✅ All statements processed successfully!")

    df = pd.DataFrame(all_results)
    ordered_cols = [
        "file_name",
        "issuer",
        "card_last_4",
        "billing_period",
        "payment_due_date",
        "statement_date",
        "total_due",
        "min_due",
        "available_credit",
    ]
    df = df.reindex(columns=ordered_cols)

    st.subheader("📊 Extracted Summary")
    st.dataframe(df, use_container_width=True)

    # Simple visualization
    df_plot = df.dropna(subset=["total_due"])
    if not df_plot.empty:
        fig = px.bar(
            df_plot,
            x="issuer",
            y="total_due",
            color="issuer",
            title="Total Amount Due per Bank",
            text="total_due",
        )
        st.plotly_chart(fig, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Combined CSV",
        csv_data,
        file_name="parsed_credit_card_statements.csv",
        mime="text/csv",
    )

else:
    st.info("Upload up to 5 statements to begin.")
