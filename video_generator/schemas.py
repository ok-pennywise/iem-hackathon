from ninja import Schema


class GenerateScriptIn(Schema):
    topic: str


class ScriptIn(Schema):
    script: str


class AssembleIn(Schema):
    script: str
    audio_url: str
    image_urls: list[str]