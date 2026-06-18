# test_s3_real.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

from s3_service import save_results, get_results

# Step 1: Save fake analysis data to S3
fake_analysis = "This is a test analysis result for S3 verification."
result_id = save_results(fake_analysis)
print(f"Saved to S3 with result_id: {result_id}")

# Step 2: Read it back from S3
retrieved = get_results(result_id)
print("Retrieved from S3:", retrieved)

# Step 3: Confirm the data matches what we saved
assert retrieved["analysis"] == fake_analysis, "Mismatch! Data doesn't match what was saved."
print("✅ Round-trip successful — data matches.")