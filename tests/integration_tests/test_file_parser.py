from __future__ import annotations

import logging
import logging.config
import os

import pytest

import zhipuai
from zhipuai import ZhipuAI


def test_file_parser_create(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.file_parser.create(file=open('hitsuyoushorui-cn.pdf', 'rb'), file_type='pdf', tool_type='zhipu_pro')
		print(response)

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)

def test_file_parser_content(logging_conf):
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		response = client.file_parser.content(task_id="66e8f7ab884448c8b4190f251f6c2982-1", format_type="text")
		print(response.content.decode('utf-8'))

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)

