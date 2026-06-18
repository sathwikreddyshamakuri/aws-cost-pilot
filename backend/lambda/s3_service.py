# Handles saving and retrieving analysis results from S3
import boto3
import json
import uuid
import os

s3 = boto3.client("s3", region_name="us-east-1")

# Bucket name comes from environment — never hardcode bucket names
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "aws-cost-pilot-results")


def save_results(analysis):
    # Generate a unique ID so concurrent users never collide
    result_id = str(uuid.uuid4())

    # Store as JSON so it's easy to parse back later
    data = {
        "result_id": result_id,
        "analysis": analysis
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"results/{result_id}.json",
        Body=json.dumps(data),
        ContentType="application/json"
    )

    return result_id


def get_results(result_id):
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=f"results/{result_id}.json"
    )

    # S3 returns a streaming body — must read and decode before parsing JSON
    body = response["Body"].read().decode("utf-8")
    return json.loads(body) 
