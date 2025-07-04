import logging
import logging.config

import zhipuai
from zhipuai import ZhipuAI


def test_tools(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.tools.web_search(
			model='web-search-pro',
			messages=[
				{
					'content': '你好',
					'role': 'user',
				}
			],
			stream=False,
		)
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_tools_stream(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.tools.web_search(
			model='web-search-pro',
			messages=[
				{
					'content': '你好',
					'role': 'user',
				}
			],
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
