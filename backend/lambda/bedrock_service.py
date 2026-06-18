# bedrock_service.py
import boto3
import json
import os

# Bedrock runtime is separate from the main Bedrock client
bedrock = boto3.client("bedrock-runtime")

# Using Claude 3 Sonnet on Bedrock — good balance of speed and quality
MODEL_ID = os.getenv("BEDROCK_MODEL_ID","anthropic.claude-3-sonnet-20240229-v1:0")


def analyze_costs(extracted_text):
    prompt = build_prompt(extracted_text)

    # Bedrock uses a standard messages API similar to Anthropic's direct API
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    # Response body is a streaming object — read and parse it
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def build_prompt(extracted_text):
    # A specific, structured prompt gets far better results than a vague one
    return f"""You are an AWS cost optimization expert helping a Finance team.

Analyze the following AWS bill and provide:
1. Top 3 most expensive services and what is driving their cost
2. Any unusual spikes or patterns compared to typical usage
3. Specific actionable recommendations to reduce costs
4. Estimated monthly savings if recommendations are followed

Format your response as structured sections with clear headings.
Be specific — mention actual service names and dollar amounts from the bill.

AWS Bill Data:
{extracted_text}
""" 
