from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config


def test_transcriptions(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        with open("asr1.wav", "rb") as audio_file:
            transcriptResponse = client.audio.transcriptions.create(
                model="glm-asr",
                file=audio_file,
                stream=False
            )
            print(transcriptResponse)
    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_transcriptions_stream(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        with open("asr1.wav", "rb") as audio_file:
            transcriptResponse = client.audio.transcriptions.create(
                model="glm-asr",
                file=audio_file,
                stream=True
            )
            for item in transcriptResponse:
                print(item)
    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

