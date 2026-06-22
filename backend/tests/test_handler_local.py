# test_handler_local.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda"))
from unittest.mock import patch
from handler import lambda_handler

# Fake event simulating what API Gateway would send for POST /analyze
fake_event = {
    "requestContext": {
        "http": {
            "method": "POST",
            "path": "/analyze"
        }
    },
    "headers": {"Content-Type": "text/csv"},
    "body": "U2VydmljZSxDb3N0..."
}

# Patch the real functions so they never actually run
with patch("handler.extract_text", return_value="fake extracted text"), \
     patch("handler.analyze_costs", return_value="fake analysis result"), \
     patch("handler.save_results", return_value="fake-result-id-123"):

    result = lambda_handler(fake_event, None)
    print("Status code:", result["statusCode"])
    print("Body:", result["body"])