from uuid import uuid4
from django.conf import settings
from ninja import Router
import requests

from security.authentication import JWTBearer
from video_generator import schemas
import gtts
import os

router: Router = Router(auth=JWTBearer())


@router.post("/generate-script", auth=None)
def generate_script(request, schema: schemas.GenerateScriptIn) -> dict[str, str]:
    key: str = getattr(settings, "GEMINI_API_KEY")
    url: str = (
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    )
    headers: dict[str, str] = {"Content-Type": "application/json"}

    prompt: str = f"Create a school lesson on {schema.topic} with simple explanations. Must be short"
    data: dict[str, list[dict[str, list[dict[str, str]]]]] = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Print response
    if response.status_code == 200:
        return {
            "script": response.json()["candidates"][0]["content"]["parts"][0]["text"]
        }
    else:
        return {"error": "Something went wrong"}


@router.post("/generate-voice", auth=None)
def generate_voice(request, schema: schemas.ScriptIn) -> dict[str, str]:
    # Define the audio directory
    audio_dir: str = "media/audio"

    # Create the directory if it doesn't exist
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    # Generate the speech
    tts = gtts.gTTS(text=schema.script, lang="en")

    # Create a unique filename and save the audio file
    audio_path = os.path.join(audio_dir, f"{uuid4()}.mp3")
    tts.save(audio_path)

    return {"audio_url": audio_path}


@router.post("/generate-visuals")
def generate_script(request, schema: schemas.ScriptIn) -> dict[str, list[str]]:
    return {"image_urls": []}


@router.post("/assemble")
def generate_script(request, schema: schemas.AssembleIn) -> dict[str, str]:
    return {"video_url": ""}
