from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config

def test_audio_speech(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.audio.speech(
            model="cogtts",
            input="智谱ai，你好呀",
            voice="female",
            response_format="wav"
        )
        print(response)
        with open("output.wav", "wb") as f:
            f.write(response.content)
        print("文件已保存为 output.wav")

    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

def test_audio_customization(logging_conf):
    logging.config.dictConfig(logging_conf)
    client = ZhipuAI()  # 填写您自己的APIKey
    with open('/Users/jhy/Desktop/tts/test_case_8s.wav', 'rb') as file:
        try:
            response = client.audio.customization(
                model="cogtts",
                input="智谱ai，你好呀",
                voice_text="这是一条测试用例",
                voice_data=file,
                response_format="wav"
            )
            print(response)
            with open("output.wav", "wb") as f:
                f.write(response.content)
            print("文件已保存为 output.wav")

        except zhipuai.core._errors.APIRequestFailedError as err:
            print(err)
        except zhipuai.core._errors.APIInternalError as err:
            print(err)
        except zhipuai.core._errors.APIStatusError as err:
            print(err)
