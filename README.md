# AWS Cost Pilot

An AI-powered AWS cost analyzer that turns a raw AWS billing PDF or CSV into a clear, actionable savings plan — built for Finance teams who don't want to dig through line-item billing data themselves.

**🔗 Live demo:** https://aws-cost-pilot.vercel.app

---

## What it does

1. Upload an AWS bill (PDF or CSV)
2. The system extracts the billing data using **Amazon Textract**
3. **Amazon Bedrock** (Claude Sonnet 4.5) analyzes the bill and generates a structured cost optimization report
4. Results are saved to **S3** and displayed instantly — no login, no setup

The output isn't a generic summary — it's a consistently formatted report with top cost drivers, a key concern, ranked recommendations with estimated savings, and a total savings projection.

---

## Architecture

```
React (Vercel)
      │
      ▼
API Gateway (HTTP API)
      │
      ▼
AWS Lambda  ──────►  Amazon Textract   (extract text from PDF/CSV)
      │
      ▼
Amazon Bedrock        (Claude Sonnet 4.5 — cost analysis)
      │
      ▼
Amazon S3             (store results)
```

**Backend:** Python (AWS Lambda), boto3
**AI/ML:** Amazon Bedrock (Claude Sonnet 4.5), Amazon Textract
**Infrastructure:** API Gateway (HTTP API), S3, IAM
**Frontend:** React + Vite + Tailwind CSS, deployed on Vercel

---

## Why these design decisions

- **IAM least privilege:** the Lambda execution role is split into 4 separate, scoped policies (S3, Textract, Bedrock, CloudWatch Logs) rather than one broad policy — each grants only the specific actions needed, on only the specific resources needed.
- **HTTP API over REST API:** chosen for lower cost and lower latency on this simple two-route API; native CORS support meant less manual configuration than REST API would have required.
- **Prompt engineering for structure, not just content:** the Bedrock prompt enforces an exact output template (fixed headers, one-line bullet constraints) rather than relying on a word-count instruction — this keeps responses fast, consistent, and easy to render, and kept generation time safely under API Gateway's 30-second integration timeout.
- **No login/auth:** deliberately scoped out — this pilot focuses on demonstrating the AI/cloud pipeline, not authentication, which doesn't add to that story.

---

## Real bugs found and fixed during development

Documenting these because debugging real, deployed AWS issues is as valuable a signal as the working feature itself:

1. **HTTP API event format mismatch** — `event["httpMethod"]` (REST API format) doesn't exist on HTTP API payloads; the method/path are nested under `event["requestContext"]["http"]`.
2. **API Gateway's 30-second hard timeout** — an initial Bedrock prompt produced long, detailed responses that occasionally exceeded API Gateway's non-configurable 30s integration timeout. Fixed by redesigning the prompt to enforce a fixed, concise output structure.
3. **Missing CORS preflight handling** — browser preflight `OPTIONS` requests were hitting the Lambda's 404 fallback instead of receiving proper CORS headers; fixed using API Gateway's native CORS configuration.
4. **Double Base64 encoding** — the frontend was pre-encoding file uploads to Base64 before sending them, but API Gateway *also* Base64-encodes binary content based on `Content-Type`, resulting in doubly-encoded data that Textract rejected. Fixed by sending the raw file and letting API Gateway handle encoding via the `isBase64Encoded` flag.

---

## Project structure

```
aws-cost-pilot/
├── backend/
│   ├── lambda/              # Lambda function code
│   │   ├── handler.py           # Entry point + routing
│   │   ├── textract_service.py  # PDF/CSV text extraction
│   │   ├── bedrock_service.py   # AI cost analysis
│   │   └── s3_service.py        # Result storage/retrieval
│   └── tests/                # Local + real-AWS test scripts
├── frontend/
│   └── src/
│       ├── App.jsx              # Screen state controller
│       └── components/
│           ├── Dashboard.jsx    # Upload screen
│           ├── ProgressMap.jsx  # Pipeline progress + API call
│           └── Results.jsx      # Rendered analysis + recommendations
└── deploy.bat                 # Automated Lambda packaging + deployment
```

---

## Running locally

**Backend:**
```bash
cd backend/lambda
pip install -r requirements.txt
# Configure AWS credentials via `aws configure`
# Set environment variables in a `.env` file (see .env.example)
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Future improvements

- Download analysis as PDF
- Async processing with live backend status polling (rather than a single blocking request) for larger, multi-page bills
- Async Textract (`start_document_text_detection`) to support multi-page PDF bills
- GitHub Actions CI for automated testing and deployment

---

## About this project

Built as a hands-on learning project to understand AWS Lambda, API Gateway, Bedrock, Textract, and IAM in depth — every architectural decision above was deliberately made and tested against real AWS infrastructure, not just designed on paper.