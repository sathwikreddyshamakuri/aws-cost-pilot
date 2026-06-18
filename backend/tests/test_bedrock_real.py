# test_bedrock_real.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

from bedrock_service import analyze_costs

sample_bill_text = """
AWS Billing Summary - May 2026
EC2: $450.00
S3: $32.50
Lambda: $12.00
RDS: $210.00
Data Transfer: $45.00
"""

result = analyze_costs(sample_bill_text)
print("=== Bedrock Analysis Result ===")
print(result)