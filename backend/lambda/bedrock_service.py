# bedrock_service.py
import boto3
import json
import os

# Bedrock runtime is separate from the main Bedrock client
bedrock = boto3.client("bedrock-runtime")

# Using Claude 3 Sonnet on Bedrock — good balance of speed and quality
MODEL_ID = os.getenv("BEDROCK_MODEL_ID","us.anthropic.claude-sonnet-4-5-20250929-v1:0")


def analyze_costs(extracted_text):
    prompt = build_prompt(extracted_text)

    # Bedrock uses a standard messages API similar to Anthropic's direct API
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 800,
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
    return f"""You are an AWS cost optimization expert advising a Finance team. Time is limited, so be direct and skip preamble.

Analyze this AWS bill and respond in EXACTLY this format, with no extra commentary before or after:

## Top Cost Drivers
- [Service Name]: $[amount] — [cost driver in ≤10 words]
- [Service Name]: $[amount] — [cost driver in ≤10 words]
- [Service Name]: $[amount] — [cost driver in ≤10 words]

## Key Concern
[One sentence flagging the single biggest optimization opportunity]

## Recommendations
1. [Action] → Est. savings: $[amount]/month
2. [Action] → Est. savings: $[amount]/month
3. [Action] → Est. savings: $[amount]/month

## Total Estimated Savings
$[amount]/month ([percentage]% of current bill)

Rules:
- Each bullet/line must fit on one line — no sub-explanations, no paragraphs
- Use only real numbers from the bill provided — never invent figures
- Skip any service with cost under $5 unless it's the only option

AWS Bill Data:
{extracted_text}
"""
