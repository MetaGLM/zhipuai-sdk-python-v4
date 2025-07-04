def test_sdk_import_unit():
	import zhipuai

	print(zhipuai.__version__)


def test_os_import_unit():
	import os

	print(os)


def test_sdk_import():
	from zhipuai import ZhipuAI

	client = ZhipuAI(api_key='empty')  # 请填写您自己的APIKey

	if client is not None:
		print('SDK导入成功')
	else:
		print('SDK导入失败')
