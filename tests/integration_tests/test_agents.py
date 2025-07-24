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

def test_correction():
	client = ZhipuAI()  # 请替换为实际API密钥

	response = client.agents.invoke(
		agent_id="intelligent_education_correction_agent",
		messages=[
				{
					"role": "user",
					"content": [
						{
							"type": "image_url",
							"image_url": "https://b0.bdstatic.com/e24937f1f6b9c0ff6895e1012c981515.jpg"
						}
					]
				}
			]
		)
	print(response)
 
def test_correction_result(image_id,uuids,trace_id):
	client = ZhipuAI()

	response = client.agents.async_result(
		agent_id="intelligent_education_correction_polling",
		custom_variables={
				"images": [
					{
						"image_id": image_id,
						"uuids": uuids
					}
				],
				"trace_id": trace_id
		}
	)
	print(response)
 
def main():
    test_completions_sync()
    test_completions_stream()
    # test_correction()
	# test_correction_result(image_id,uuids,trace_id)

if __name__ == "__main__":
	main()