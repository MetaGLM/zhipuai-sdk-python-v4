import os
import pytest
from zhipuai.api_resource.tts import TTSApi

# 请根据实际情况填写
BASE_URL_LIST = "http://localhost:9203"
BASE_URL_ADD = "http://localhost:9203"
API_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX3R5cGUiOiJTRVJWSUNFIiwidXNlcl9pZCI6MywiYXBpX2tleSI6IjM0ZDhiM2ExNDQ2OTQ0MmY5MTJkNzg5MTJjZjZlMjU1IiwidXNlcl9rZXkiOiIyNzQyNjM0My1iYjI0LTQ4ZDktODVjNy01ODFmMjUwNzBiMzMiLCJjdXN0b21lcl9pZCI6IjEwMDAwMyIsInVzZXJuYW1lIjoiY3BjMTk4NiJ9.3MsaFjRAyArDp2WZsVbvKGPrVjkKvGB5EfBafprcFogbDeZv4s9VCQt4wUaR4FVon1tiL_pnqtMaI6qGGXs0Qg"
AUDIO_FILE_PATH = r"C:\Users\zjq18\Downloads\北京今天的天气.wav"

@pytest.mark.integration
def test_list_voices():
    tts_api = TTSApi(base_url=BASE_URL_LIST, api_key=API_TOKEN)
    resp = tts_api.list_voices()
    assert resp.code == 200
    assert resp.success
    assert isinstance(resp.data, list)
    if resp.data:
        assert hasattr(resp.data[0], "voiceId")

@pytest.mark.integration
def test_add_voice():
    if not os.path.exists(AUDIO_FILE_PATH):
        pytest.skip("音频文件不存在，跳过上传测试")
    tts_api = TTSApi(base_url=BASE_URL_ADD, api_key=API_TOKEN)
    resp = tts_api.add_voice(
        voice_name="磁性嗓音123",
        voice_text="今天北京的天气怎么样？",
        file_path=AUDIO_FILE_PATH
    )
    assert resp.code == 200
    assert resp.success
    assert resp.data.voiceName == "磁性嗓音123" 