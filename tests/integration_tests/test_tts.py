import os
import pytest
from zhipuai.api_resource.tts import TTSApi

# 请根据实际情况填写
BASE_URL_LIST = "https://dev.bigmodel.cn/stage-api/paas/v4"
BASE_URL_ADD = "https://dev.bigmodel.cn/stage-api/paas/v4"
API_KEY = "d91103df5c4a47bb808d4c84bcae9fcf.HCFkuDBhwKWLxliY"
AUDIO_FILE_PATH = r"C:\Users\zjq18\Downloads\北京今天的天气.wav"

@pytest.mark.integration
def test_list_voices():
    tts_api = TTSApi(base_url=BASE_URL_LIST, api_key=API_KEY)
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
    tts_api = TTSApi(base_url=BASE_URL_ADD, api_key=API_KEY)
    resp = tts_api.add_voice(
        voice_name="磁性嗓音123",
        voice_text="今天北京的天气怎么样？",
        file_path=AUDIO_FILE_PATH
    )
    assert resp.code == 200
    assert resp.success
    assert resp.data.voiceName == "磁性嗓音123" 