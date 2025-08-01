import base64
import json
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
			voice='tongtong',
			stream=False,
			response_format='wav',
		)
		response.stream_to_file(speech_file_path)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)

def test_audio_speech_streaming(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.audio.speech(
			model='cogtts',
			input='你好呀,欢迎来到智谱开放平台',
			voice='tongtong',
			stream=True,
			response_format='mp3',
			encode_format='hex'
		)
		with open("output.pcm", "wb") as f:
			for item in response:
				choice = item.choices[0]
				index = choice.index
				finish_reason = choice.finish_reason
				audio_delta = choice.delta.content
				if finish_reason is not None:
					break
				f.write(base64.b64decode(audio_delta))
				print(f"{index}.finish_reason = {finish_reason}, audio_delta = {len(audio_delta)}")

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)
	except Exception as e:
		print(e)


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
