import logging
import logging.config

import zhipuai
from zhipuai import ZhipuAI


def test_images(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.images.generations(
			model='cogview-3',  # 填写需要调用的模型名称
			prompt='一只可爱的小猫咪',
			extra_body={'user_id': '1222212'},
			user_id='12345678',
		)
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_images_sensitive_word_check(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.images.generations(
			model='cogview-3',  # 填写需要调用的模型名称
			prompt='一只可爱的小猫咪',
			sensitive_word_check={'type': 'ALL', 'status': 'DISABLE'},
			extra_body={'user_id': '1222212'},
			user_id='12345678',
		)
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)
