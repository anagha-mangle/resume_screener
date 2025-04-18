
# resume_parser.py

import os
import fitz  # PyMuPDF for PDF files
import docx  # python-docx for DOCX files

def extract_text_from_pdf(file_path):
    """Extract text from a PDF using PyMuPDF (fitz)."""
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"[PDF Error] {e}")
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file using python-docx."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"[DOCX Error] {e}")
    return text

def extract_text_from_file(file_path):
    """
    Detect file extension and extract text accordingly.
    Supports: PDF and DOCX
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return "[Unsupported file type. Only PDF and DOCX are supported.]"
