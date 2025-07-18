import logging
import logging.config

import zhipuai
from zhipuai import ZhipuAI


def test_assistant(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		generate = client.assistant.conversation(
			assistant_id='659e54b1b8006379b4b2abd6',
			messages=[
				{
					'role': 'user',
					'content': [{'type': 'text', 'text': '帮我搜索下智谱的cogvideox发布时间'}],
				}
			],
			stream=True,
			attachments=None,
			metadata=None,
			request_id='request_1790291013237211136',
			user_id='12345678',
		)
		for assistant in generate:
			print(assistant)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_assistant_query_support(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.assistant.query_support(
			assistant_id_list=[],
			request_id='request_1790291013237211136',
			user_id='12345678',
		)
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_assistant_query_conversation_usage(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.assistant.query_conversation_usage(
			assistant_id='659e54b1b8006379b4b2abd6',
			request_id='request_1790291013237211136',
			user_id='12345678',
		)
		print(response)
	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_translate_api(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		translate_response = client.assistant.conversation(
			assistant_id='9996ijk789lmn012o345p999',
			messages=[{'role': 'user', 'content': [{'type': 'text', 'text': '你好呀'}]}],
			stream=True,
			attachments=None,
			metadata=None,
			request_id='request_1790291013237211136',
			user_id='12345678',
			extra_parameters={'translate': {'from': 'zh', 'to': 'en'}},
		)
		for chunk in translate_response:
			print(chunk.choices[0].delta)
		# print(translate_response)
	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)
