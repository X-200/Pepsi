#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import re
import arabic_reshaper
from bidi.algorithm import get_display

# Read the DOCX file
doc = Document('/vercel/sandbox/uploads/MCQs on systematic مختصرة.docx')

# Extract all text
full_text = []
for para in doc.paragraphs:
    text = para.text.strip()
    if text:
        full_text.append(text)

# Print extracted text for analysis
print("=== Extracted Text ===")
for i, line in enumerate(full_text[:50]):  # Print first 50 lines
    print(f"{i}: {line}")

print(f"\nTotal lines: {len(full_text)}")
