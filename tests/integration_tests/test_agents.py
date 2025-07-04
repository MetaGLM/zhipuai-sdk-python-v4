import logging
import logging.config
import time

import zhipuai
from zhipuai import ZhipuAI


def test_completions_sync(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		# 生成request_id
		request_id = time.time()
		print(f'request_id:{request_id}')
		response = client.agents.invoke(
			request_id=request_id,
			agent_id='general_translation',
			messages=[{'role': 'user', 'content': 'tell me a joke'}],
			user_id='12345678',
		)
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_completions_stream(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		# 生成request_id
		request_id = time.time()
		print(f'request_id:{request_id}')
		response = client.agents.invoke(
			request_id=request_id,
			agent_id='general_translation',
			messages=[{'role': 'user', 'content': 'tell me a joke'}],
			user_id='12345678',
			stream=True,
		)
		for item in response:
			print(item)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)
