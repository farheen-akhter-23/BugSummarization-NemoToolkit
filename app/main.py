# app/main.py
import streamlit as st
import requests
import json
from PIL import Image
import fitz  # PyMuPDF for PDF processing
import io

# Set up Streamlit UI
st.set_page_config(page_title="Bug Report Summarization", layout="wide")
st.title("Bug Report Summarization")

# Sidebar for Query History
st.sidebar.title("Query History")
history = st.sidebar.empty()

def display_summary(summary):
    st.subheader("Summary")
    st.write(summary)

# Upload Functionality
uploaded_file = st.file_uploader("Upload a Bug Report (PDF or PNG)", type=["pdf", "png"])

if uploaded_file:
    # Check file type
    if uploaded_file.type == "application/pdf":
        # PDF processing
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
    elif uploaded_file.type == "image/png":
        # PNG processing
        img = Image.open(uploaded_file)
        text = pytesseract.image_to_string(img)

    # Send the text to the FastAPI backend
    response = requests.post("http://localhost:8000/summarize", json={"text": text})
    summary = response.json().get("summary")
    display_summary(summary)
    
    # Update query history
    history_response = requests.get("http://localhost:8000/history")
    history.write(history_response.json())

