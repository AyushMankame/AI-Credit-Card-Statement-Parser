import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_like):
    text = ""
    file_like.seek(0)
    with pdfplumber.open(file_like) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

def extract_text_with_ocr_if_needed(file_like):
    file_like.seek(0)
    full_text = ""
    with pdfplumber.open(file_like) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=200).original
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"
    return full_text
