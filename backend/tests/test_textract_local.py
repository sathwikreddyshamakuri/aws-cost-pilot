# test_textract_local.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda"))
from textract_service import extract_from_csv

sample_csv = b"""Service,Cost
EC2,120.50
S3,15.30
Lambda,5.00
"""

result = extract_from_csv(sample_csv)
print("Extracted text:")
print(result)