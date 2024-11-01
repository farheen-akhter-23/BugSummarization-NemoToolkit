
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_png(png_bytes):
    img = Image.open(io.BytesIO(png_bytes))
    return pytesseract.image_to_string(img)
