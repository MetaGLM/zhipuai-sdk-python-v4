import os
import logging
import logging.config
from zhipuai import ZhipuAI


def test_batch_input_file(test_file_path, logging_conf) -> None:
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey

    batch_input_file = client.files.create(
        file=open(os.path.join(test_file_path, "batchinput.jsonl"), "rb"),
        purpose="batch"
    )

    print(batch_input_file)


#     FileObject(id='file-1w226DCBIAWg0obmdWHRXLhl', bytes=490, created_at=1715593897, filename='batchinput.jsonl', object='file', purpose='batch', status='processed', status_details=None)
#     FileObject(id='file-MlVVOdCeGXu03QkoPOEfPdD3', bytes=490, created_at=1715395228, filename='batchinput.jsonl', object='file', purpose='batch', status='processed', status_details=None)


def test_batch_create(logging_conf) -> None:
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey

    create = client.batches.create(
        input_file_id="file-MlVVOdCeGXu03QkoPOEfPdD3",
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "nightly eval job22222"
        }
    )
    print(create)
    # Batch(id='batch_jaJkXUJJJ3212wTQ5Hd2jI1M', completion_window='24h', created_at=1715395401, endpoint='/v1/chat/completions', input_file_id='file-MlVVOdCeGXu03QkoPOEfPdD3', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1715481801, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'nightly eval job'}, output_file_id=None, request_counts=BatchRequestCounts(completed=0, failed=0, total=0))
    #     Batch(id='batch_eOnnpIb3yykbOc5fEg7ctc51', completion_window='24h', created_at=1715396371, endpoint='/v1/chat/completions', input_file_id='file-MlVVOdCeGXu03QkoPOEfPdD3', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1715482771, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'nightly eval job22222'}, output_file_id=None, request_counts=BatchRequestCounts(completed=0, failed=0, total=0))


def test_batch_retrieve(logging_conf) -> None:
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey

    retrieve = client.batches.retrieve("batch_eOnnpIb3yykbOc5fEg7ctc51")
    print(retrieve)
    # Batch(id='batch_jaJkXUJJJ3212wTQ5Hd2jI1M', completion_window='24h', created_at=1715395401, endpoint='/v1/chat/completions', input_file_id='file-MlVVOdCeGXu03QkoPOEfPdD3', object='batch', status='in_progress', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1715481801, failed_at=None, finalizing_at=None, in_progress_at=1715395401, metadata={'description': 'nightly eval job'}, output_file_id=None, request_counts=BatchRequestCounts(completed=2, failed=0, total=2))


def test_batch_cancel(logging_conf) -> None:
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey

    cancel = client.batches.cancel("batch_jaJkXUJJJ3212wTQ5Hd2jI1M")
    print(cancel)
    # Batch(id='batch_jaJkXUJJJ3212wTQ5Hd2jI1M', completion_window='24h', created_at=1715395401, endpoint='/v1/chat/completions', input_file_id='file-MlVVOdCeGXu03QkoPOEfPdD3', object='batch', status='cancelling', cancelled_at=None, cancelling_at=1715396130, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1715481801, failed_at=None, finalizing_at=None, in_progress_at=1715395401, metadata={'description': 'nightly eval job'}, output_file_id=None, request_counts=BatchRequestCounts(completed=2, failed=0, total=2))


def test_batch_list(logging_conf) -> None:
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey

    list = client.batches.list(limit=10)
    print(list)


#     SyncCursorPage[Batch](data=[Batch(id='batch_jaJkXUJJJ3212wTQ5Hd2jI1M', completion_window='24h', created_at=1715395401, endpoint='/v1/chat/completions', input_file_id='file-MlVVOdCeGXu03QkoPOEfPdD3', object='batch', status='cancelling', cancelled_at=None, cancelling_at=1715396130, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1715481801, failed_at=None, finalizing_at=None, in_progress_at=1715395401, metadata={'description': 'nightly eval job'}, output_file_id=None, request_counts=BatchRequestCounts(completed=2, failed=0, total=2))], object='list', first_id='batch_jaJkXUJJJ3212wTQ5Hd2jI1M', last_id='batch_jaJkXUJJJ3212wTQ5Hd2jI1M', has_more=False)


def test_batch_result(test_file_path, logging_conf) -> None:
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey

    content = client.files.content("file-QDpVyDIhxj8mcFiduUydNqQN")
    with open(os.path.join(test_file_path, "batchoutput.jsonl"), "wb") as f:
        f.write(content.content)
