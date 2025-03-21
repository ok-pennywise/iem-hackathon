from uuid import uuid4
from ninja import Router

from security.authentication import JWTBearer
from video_generator import schemas
import gtts
import os

router: Router = Router(auth=JWTBearer())


@router.post("/generate-script")
def generate_script(request, schema: schemas.GenerateScriptIn) -> dict[str, str]:
    return {"script": "xyx...."}


@router.post("/generate-voice", auth=None)
def generate_voice(request, schema: schemas.ScriptIn) -> dict[str, str]:
    # Define the audio directory
    audio_dir = "media/audio"

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
