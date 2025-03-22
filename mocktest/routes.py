import json
from sys import api_version
from django.conf import settings
from ninja import Router, UploadedFile, File
import pdfplumber
import requests
from mocktest import schemas
from security.authentication import JWTBearer

router: Router = Router(auth=JWTBearer())


@router.post("/upload")
def upload(request, file: UploadedFile = File(...)) -> dict[str, str]:
    with pdfplumber.open(file) as pdf:
        text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )
        return {"extracted_text": text}


@router.post("/generate")
def generate_mock_test(request, schema: schemas.MockTestIn) -> dict:
    """Generate a multiple-choice mock test from extracted text"""

    prompt: str = f"""
    You are an AI that creates multiple-choice mock tests. 

    **Extracted Text:** {schema.extracted_text}

    **Instructions:**
    - Generate a list of multiple-choice questions based on the text.
    - Each question should have 4 options labeled A, B, C, D.
    - Provide the correct answer.

    **JSON Output Format:**
    {{
        "test": [
            {{
                "question": "What is Newton's first law?",
                "options": ["A body at rest...", "For every action...", "F=ma", "None"],
                "answer": "A"
            }},
            ...
        ]
    }}

    **IMPORTANT:**
    - Only return a **valid JSON object** (no extra text).
    - If no questions can be generated, return: {{ "test": [] }}
    """

    key: str = settings.GEMINI_API_KEY
    url: str = (
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    )
    headers: dict[str, str] = {"Content-Type": "application/json"}
    data: dict[str, list[dict[str, list[dict[str, str]]]]] = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response: requests.Response = requests.post(url, headers=headers, json=data)

    try:
        response_data: dict = response.json()

        # Extract AI-generated text
        ai_response_text: str = (
            response_data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )
        if not ai_response_text:
            return {"error": "Empty AI response"}

        if ai_response_text.startswith("```json"):
            ai_response_text = ai_response_text.strip("```json").strip("```")

        mock_test: dict = json.loads(ai_response_text)

        # Validate response format
        if isinstance(mock_test, dict) and "test" in mock_test:
            return mock_test
        else:
            return {"error": "AI returned invalid format"}

    except json.JSONDecodeError as e:
        return {"error": f"Parsing error: {str(e)}"}
