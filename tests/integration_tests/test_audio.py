import logging
import logging.config
from pathlib import Path

import zhipuai
from zhipuai import ZhipuAI


def test_audio_speech(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		speech_file_path = Path(__file__).parent / 'speech.wav'
		response = client.audio.speech(
			model='cogtts',
			input='你好呀,欢迎来到智谱开放平台',
			voice='female',
			response_format='wav',
		)
		response.stream_to_file(speech_file_path)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_audio_customization(logging_conf):
	logging.config.dictConfig(logging_conf)
	client = ZhipuAI()  # 填写您自己的APIKey
	with open(Path(__file__).parent / 'speech.wav', 'rb') as file:
		try:
			speech_file_path = Path(__file__).parent / 'speech.wav'
			response = client.audio.customization(
				model='cogtts',
				input='你好呀,欢迎来到智谱开放平台',
				voice_text='这是一条测试用例',
				voice_data=file,
				response_format='wav',
			)
			response.stream_to_file(speech_file_path)

		except zhipuai.core._errors.APIRequestFailedError as err:
			print(err)
		except zhipuai.core._errors.APIInternalError as err:
			print(err)
		except zhipuai.core._errors.APIStatusError as err:
			print(err)
