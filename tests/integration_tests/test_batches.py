import logging
import logging.config
import os

import zhipuai
from zhipuai import ZhipuAI


def test_batch_input_file(test_file_path, logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey

	try:
		batch_input_file = client.files.create(
			file=open(os.path.join(test_file_path, 'batchinput.jsonl'), 'rb'),
			purpose='batch',
		)

		print(batch_input_file)

	#   FileObject(id='20240514_ea19d21b-d256-4586-b0df-e80a45e3c286', bytes=490, created_at=1715673494, filename=None, object='file', purpose='batch', status=None, status_details=None, fileName='batchinput.jsonl')

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_batch_create(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		create = client.batches.create(
			input_file_id='20240514_ea19d21b-d256-4586-b0df-e80a45e3c286',
			endpoint='/v4/chat/completions',
			completion_window='24h',
			metadata={'description': 'job test'},
			auto_delete_input_file=True,
		)
		print(create)
		# Batch(id='batch_1790292763050508288', completion_window='24h', created_at=1715674031399, endpoint='/v4/chat/completions', input_file_id='20240514_ea19d21b-d256-4586-b0df-e80a45e3c286', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=None, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'job test'}, output_file_id=None, request_counts=BatchRequestCounts(completed=None, failed=None, total=None))

	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_batch_retrieve(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		retrieve = client.batches.retrieve('batch_1790291013237211136')
		print(retrieve)

	#   Batch(id='batch_1790291013237211136', completion_window='24h', created_at=1715673614000, endpoint='/v4/chat/completions', input_file_id='20240514_ea19d21b-d256-4586-b0df-e80a45e3c286', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id='', errors=None, expired_at=None, expires_at=None, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'job test'}, output_file_id='', request_counts=BatchRequestCounts(completed=None, failed=None, total=None))
	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_batch_cancel(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		cancel = client.batches.cancel('batch_1790291013237211136')
		print(cancel)
		# Batch(id='batch_1790291013237211136', completion_window='24h', created_at=1715673614000, endpoint='/v4/chat/completions', input_file_id='20240514_ea19d21b-d256-4586-b0df-e80a45e3c286', object='batch', status='cancelling', cancelled_at=None, cancelling_at=1715673698775, completed_at=None, error_file_id='', errors=None, expired_at=None, expires_at=None, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'job test'}, output_file_id='', request_counts=BatchRequestCounts(completed=None, failed=None, total=None))
	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_batch_list(logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		list = client.batches.list(limit=10)
		print(list)
		if list.has_more:
			print('_________get_next_page___________')
			batch = list.get_next_page()
			print(batch)
			print('_________iter_pages___________')
			for batch in list.iter_pages():
				print(batch)
	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)


def test_batch_result(test_file_path, logging_conf) -> None:
	logging.config.dictConfig(logging_conf)  # type: ignore
	client = ZhipuAI()  # 填写您自己的APIKey
	try:
		content = client.files.content('file-QDpVyDIhxj8mcFiduUydNqQN')
		with open(os.path.join(test_file_path, 'content_batchoutput.jsonl'), 'wb') as f:
			f.write(content.content)
		content.write_to_file(os.path.join(test_file_path, 'write_to_file_batchoutput.jsonl'))

		assert (
			content.content == open(os.path.join(test_file_path, 'batchoutput.jsonl'), 'rb').read()
		)
		assert (
			content.content
			== open(os.path.join(test_file_path, 'write_to_file_batchoutput.jsonl'), 'rb').read()
		)
	except zhipuai.core._errors.APIRequestFailedError as err:
		print(err)
	except zhipuai.core._errors.APIInternalError as err:
		print(err)
	except zhipuai.core._errors.APIStatusError as err:
		print(err)
