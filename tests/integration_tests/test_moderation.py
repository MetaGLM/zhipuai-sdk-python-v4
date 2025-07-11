import logging
import logging.config
import time

import zhipuai
from zhipuai import ZhipuAI


def test_completions_temp0(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI(disable_token_cache=False)  # 填写您自己的APIKey
	try:
		# 生成request_id
		request_id = time.time()
		print(f'request_id:{request_id}')
		response = client.moderations.create(
			model='moderations', input={'type': 'text', 'text': 'hello world '}
		)
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)
