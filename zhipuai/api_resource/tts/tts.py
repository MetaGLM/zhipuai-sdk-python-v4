import requests
from typing import Optional
from zhipuai.types.tts.voice import VoiceListResponse, VoiceAddResponse

class TTSApi:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

    def list_voices(self) -> VoiceListResponse:
        url = f"{self.base_url}/voice/list"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        resp = requests.post(url,headers=headers)
        resp.raise_for_status()
        return VoiceListResponse.parse_obj(resp.json())

    def add_voice(self, voice_name: str, voice_text: str, file_path: str) -> VoiceAddResponse:
        url = f"{self.base_url}/voice/add"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        files = {
            "voiceName": (None, voice_name),
            "voiceText": (None, voice_text),
            "file": open(file_path, "rb"),
        }
        resp = requests.post(url, headers=headers, files=files)
        resp.raise_for_status()
        return VoiceAddResponse.parse_obj(resp.json()) 