import boto3
import csv
import io

# boto3 is the AWS SDK for Python — this creates a Textract client
textract = boto3.client("textract")

def extract_text(file_data, content_type):
    if "csv" in content_type:
        return extract_from_csv(file_data)
    else:
        return extract_from_pdf(file_data)


def extract_from_pdf(file_data):
    # Textract's detect_document_text takes raw bytes and returns blocks of text
    response = textract.detect_document_text(
        Document={"Bytes": file_data}
    )

    # Textract returns many block types — we only want the actual text lines
    lines = []
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            lines.append(block["Text"])

    # TODO: handle multi-page PDFs later using start_document_text_detection
    return "\n".join(lines)


def extract_from_csv(file_data):
    # CSV is plain text so no AI extraction needed — just decode and read it
    text = file_data.decode("utf-8")
    reader = csv.reader(io.StringIO(text))

    rows = []
    for row in reader:
        rows.append(", ".join(row))

    return "\n".join(rows) 
