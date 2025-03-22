from django.conf import settings
from ninja import Router
import requests

from doubt_solver import schemas


router: Router = Router()

@router.post("/ask")
def ask_doubt(request, schema: schemas.DoubtIn):
    key: str = getattr(settings, "GEMINI_API_KEY")
    url: str = (
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    )
    headers: dict[str, str] = {"Content-Type": "application/json"}

    prompt: str = f"""Answer this quest - \"{schema.question}\" with simple explanations. Must be short.
        ***IMPORTANT***
        Do not add any other texts apart from the answer
       """
    data: dict[str, list[dict[str, list[dict[str, str]]]]] = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Print response
    if response.status_code == 200:
        return {
            "answer": response.json()["candidates"][0]["content"]["parts"][0]["text"]
        }
    else:
        return {"error": "Something went wrong"}