# test_textract_real.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

from textract_service import extract_from_pdf

# Read the sample PDF we generated as raw bytes
pdf_path = os.path.join(os.path.dirname(__file__), "sample_aws_bill.pdf")
with open(pdf_path, "rb") as f:
    file_data = f.read()

print(f"PDF size: {len(file_data)} bytes")
print("Sending to Textract...")

result = extract_from_pdf(file_data)

print("=== Textract Extraction Result ===")
print(result)