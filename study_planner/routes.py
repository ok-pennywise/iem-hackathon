import json
from django.conf import settings
from ninja import File, Router
from ninja.files import UploadedFile
import pdfplumber
import requests

from study_planner import schemas

router: Router = Router()


@router.post("/upload")
def upload(request, file: UploadedFile = File(...)) -> dict[str, str]:
    with pdfplumber.open(file) as pdf:
        text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )
        return {"extracted_text": text}


@router.post("/generate")
def generate(request, schema: schemas.StudyPlannerIn) -> dict:
    """Generate a structured study plan using Gemini API"""

    prompt: str = f"""
    You are a study planner AI. Generate a structured study plan in **valid JSON format**.

    Syllabus: {schema.syllabus}
    Total Study Hours: {schema.study_hours}

    **JSON Format Required:**
    [
        {{"date": "2025-03-22", "topic": "Chapter 1"}},
        {{"date": "2025-03-23", "topic": "Chapter 2"}}
    ]
    
    **IMPORTANT:** 
    - Only return a **valid JSON array**. No extra text.
    - If unable to generate, return: []
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
        response_data = response.json()  # Convert response to dict

        # Extract AI-generated text
        ai_response_text = (
            response_data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        if not ai_response_text:
            return {"error": "Empty AI response"}

        # Convert text to JSON
        return ai_response_text

    except json.JSONDecodeError as e:
        return {"error": f"Parsing error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
