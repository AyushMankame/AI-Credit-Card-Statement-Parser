# 💳 Credit Card Statement Parser using AI (Gemini 2.5 Flash)

An AI-powered **Credit Card Statement Parser** that automatically extracts key financial fields from PDF statements issued by multiple banks — regardless of format, layout, or structure.

This project combines **Google Gemini 2.5 Flash** (LLM-based extraction) with traditional PDF preprocessing and cleaning to produce accurate, structured data outputs ready for analysis.

---

## 🚀 Features

- 🧠 **AI-based Extraction:** Uses Google's Gemini 2.5 Flash model to understand and extract data from PDFs.
- 📄 **Multi-bank Compatibility:** Works with statements from Axis, HDFC, IDFC First, RBL, ICICI, and more.
- 🔁 **Batch Processing:** Upload and process up to **5 PDFs simultaneously**.
- 🧹 **Smart Cleaning:** Automatically cleans currencies, dates, and fills missing values.
- 🧮 **Billing Period Inference:** Automatically calculates billing period when missing (e.g., in HDFC).
- ⚡ **Immediate Payment Handling:** Detects and defaults payment due date to `"Immediate"` if unspecified.
- 📊 **Interactive Dashboard:** View parsed results, charts, and download combined CSV.
- 💾 **Single Unified Output:** Merges all parsed results into one structured CSV file.

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend/UI** | Streamlit |
| **Backend** | Python 3.10 |
| **AI Model** | Google Gemini 2.5 Flash (via `google-genai` SDK) |
| **PDF Parsing** | pdfplumber |
| **OCR Fallback** | pytesseract |
| **Data Handling** | pandas |
| **Visualization** | plotly-express |
| **Date/Currency Cleaning** | regex + datetime |

---

## 🧩 Architecture Overview

<img width="749" height="65" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/6b09a4b0-3135-43fe-970a-6625998be5d7" />

