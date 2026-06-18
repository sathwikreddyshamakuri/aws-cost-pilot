import json
from textract_service import extract_text
from bedrock_service import analyze_costs
from s3_service import save_results

def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]

    if method == "POST" and path == "/analyze":
        return handle_analyze(event)
    elif method == "GET" and path == "/results":
        return handle_results(event)
    else:
        return response(404, {"error": "Route not found"})

def handle_analyze(event):
    import base64

    if event.get("isBase64Encoded", False):
        file_data = base64.b64decode(event["body"])
    else:
        file_data = event["body"].encode("utf-8")

    file_type = event["headers"].get("content-type", "application/pdf")

    extracted_text = extract_text(file_data, file_type)
    analysis = analyze_costs(extracted_text)
    result_id = save_results(analysis)

    return response(200, {"result_id": result_id, "analysis": analysis})


def handle_results(event):
    from s3_service import get_results
    from botocore.exceptions import ClientError

    result_id = event["queryStringParameters"]["result_id"]

    try:
        results = get_results(result_id)
        return response(200, results)
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return response(404, {"error": "Result not found"})
        else:
            return response(500, {"error": "Something went wrong"})


def response(status_code, body):
    # Lambda must always return this exact shape for API Gateway to understand it
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"  # allows React frontend to call this
        },
        "body": json.dumps(body)
    } 
