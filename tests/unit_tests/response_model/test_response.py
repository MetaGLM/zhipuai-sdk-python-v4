# -*- coding: utf-8 -*-
import unittest
from typing import Type, cast, Iterable
import pytest
import httpx
import inspect

import pydantic
from zhipuai.core import BaseModel, StreamResponse, get_args, HttpClient, construct_type
from zhipuai.core._base_type import ResponseT, ModelBuilderProtocol
from zhipuai.core._response import HttpResponse
from zhipuai.types.chat.async_chat_completion import AsyncTaskStatus, AsyncCompletion
from zhipuai.types.chat.chat_completion import (Completion,
                                                CompletionChoice as ChatCompletionChoice,
                                                CompletionMessageToolCall as ChatCompletionMessageToolCall,
                                                CompletionUsage as ChatCompletionUsage)

from zhipuai.types.embeddings import Embedding, EmbeddingsResponded
from zhipuai.types.file_object import FileObject, ListOfFileObject
from zhipuai.types.fine_tuning import FineTuningJobEvent
from zhipuai.types.fine_tuning.fine_tuning_job import FineTuningJob, ListOfFineTuningJob, Error
from zhipuai.types.fine_tuning.fine_tuning_job_event import Metric, JobEvent
from zhipuai.types.fine_tuning.job_create_params import Hyperparameters
from zhipuai.types.fine_tuning.fine_tuning_job import Hyperparameters as FineTuningHyperparameters
from zhipuai.types.fine_tuning.models import FineTunedModelsStatus
from zhipuai.types.image import GeneratedImage, ImagesResponded


class MockClient:
    def _process_response_data(
            self,
            *,
            data: object,
            cast_type: Type[ResponseT],
            response: httpx.Response,
    ) -> ResponseT:
        pass


@pytest.mark.parametrize(
    "R",
    [
        AsyncTaskStatus,
        AsyncCompletion,
        Completion,

    ],
)
def test_response_chat_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content="""{
    "id": "completion123",
    "request_id": "request456",
    "model": "model-name",
    "task_status": "completed",
    "choices": [
      {
        "index": 0,
        "finish_reason": "normal",
        "message": {
          "content": "This is the completion content.",
          "role": "assistant",
          "tool_calls": [
            {
              "id": "toolcall789",
              "function": {
                "arguments": "arg1, arg2",
                "name": "functionName"
              },
              "type": "function_call"
            }
          ]
        }
      }
    ],
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 15,
      "total_tokens": 25
    }
  }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    if R == AsyncTaskStatus:
        assert R == model.__class__
        assert isinstance(model, AsyncTaskStatus)
        assert model.id == "completion123"
        assert model.request_id == "request456"
        assert model.model == "model-name"
        assert model.task_status == "completed"


    elif R == AsyncCompletion:
        assert R == model.__class__
        assert isinstance(model, AsyncCompletion)
        assert model.id == "completion123"
        assert model.request_id == "request456"
        assert model.model == "model-name"
        assert model.task_status == "completed"
        assert isinstance(model.choices, list)
        assert model.choices[0].index == 0
        assert model.choices[0].finish_reason == "normal"
        assert model.choices[0].message.content == "This is the completion content."
        assert model.choices[0].message.role == "assistant"
        assert isinstance(model.choices[0].message.tool_calls, list)
        assert model.choices[0].message.tool_calls[0].id == "toolcall789"
        assert model.choices[0].message.tool_calls[0].function.arguments == "arg1, arg2"
        assert model.choices[0].message.tool_calls[0].function.name == "functionName"
        assert model.choices[0].message.tool_calls[0].type == "function_call"
        assert model.usage.prompt_tokens == 10
        assert model.usage.completion_tokens == 15
        assert model.usage.total_tokens == 25
    elif R == Completion:
        assert R == model.__class__
        assert isinstance(model, Completion)
        assert model.id == "completion123"
        assert model.request_id == "request456"
        assert model.model == "model-name"
        assert model.created == None
        assert isinstance(model.choices, list)
        assert isinstance(model.choices[0], ChatCompletionChoice)
        assert model.choices[0].index == 0
        assert model.choices[0].finish_reason == "normal"
        assert model.choices[0].message.content == "This is the completion content."
        assert model.choices[0].message.role == "assistant"
        assert isinstance(model.choices[0].message.tool_calls, list)
        assert isinstance(model.choices[0].message.tool_calls[0], ChatCompletionMessageToolCall)
        assert model.choices[0].message.tool_calls[0].id == "toolcall789"
        assert model.choices[0].message.tool_calls[0].function.arguments == "arg1, arg2"
        assert model.choices[0].message.tool_calls[0].function.name == "functionName"
        assert model.choices[0].message.tool_calls[0].type == "function_call"
        assert isinstance(model.usage, ChatCompletionUsage)
        assert model.usage.prompt_tokens == 10
        assert model.usage.completion_tokens == 15
        assert model.usage.total_tokens == 25

    else:
        assert False, f"Unexpected model type: {R}"

@pytest.mark.parametrize(
    "R",
    [

        FineTunedModelsStatus,

    ],
)
def test_response_finetuned_model_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content="""{
    "request_id": "12345",
    "model_name": "my-fine-tuned-model",
    "delete_status": "deleted"
  }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model, FineTunedModelsStatus)
    assert model.request_id == "12345"
    assert model.model_name == "my-fine-tuned-model"
    assert model.delete_status == "deleted"


@pytest.mark.parametrize(
    "R",
    [

        FineTuningJob,

    ],
)
def test_response_job_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content=""" {
    "id": "job123",
    "request_id": "req456",
    "created_at": 1617181723,
    "error": {
      "code": "404",
      "message": "Not Found",
      "param": "model_id"
    },
    "fine_tuned_model": "ft_model_1",
    "finished_at": 1617182000,
    "hyperparameters": {
      "n_epochs": 10
    },
    "model": "base_model",
    "object": "fine_tuning_job",
    "result_files": [
      "result1.txt",
      "result2.json"
    ],
    "status": "completed",
    "trained_tokens": 1000000,
    "training_file": "training_data.csv",
    "validation_file": "validation_data.csv"
  }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model, FineTuningJob)
    assert model.id == "job123"
    assert model.request_id == "req456"
    assert model.created_at == 1617181723
    assert isinstance(model.error, Error)
    assert model.error.code == "404"
    assert model.error.message == "Not Found"
    assert model.error.param == "model_id"
    assert model.fine_tuned_model == "ft_model_1"
    assert model.finished_at == 1617182000
    assert isinstance(model.hyperparameters, FineTuningHyperparameters)
    assert model.hyperparameters.n_epochs == 10
    assert model.model == "base_model"
    assert model.object == "fine_tuning_job"
    assert model.result_files == ["result1.txt", "result2.json"]
    assert model.status == "completed"
    assert model.trained_tokens == 1000000
    assert model.training_file == "training_data.csv"
    assert model.validation_file == "validation_data.csv"


@pytest.mark.parametrize(
    "R",
    [

        FineTuningJobEvent,

    ],
)
def test_response_joblist_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content="""{
    "object": "fine_tuning_job",
    "data": [
      {
        "object": "job_event",
        "id": "event123",
        "type": "training",
        "created_at": 1617181723,
        "level": "info",
        "message": "Training has started.",
        "data": {
          "epoch": 1,
          "current_steps": 100,
          "total_steps": 1000,
          "elapsed_time": "00:10:00",
          "remaining_time": "05:20:00",
          "trained_tokens": 500000,
          "loss": 0.05,
          "eval_loss": 0.03,
          "acc": 0.9,
          "eval_acc": 0.95,
          "learning_rate": 0.001
        }
      }
    ],
    "has_more": false
  }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model, FineTuningJobEvent)
    assert isinstance(model.data, list)
    assert isinstance(model.data[0], JobEvent)
    assert model.data[0].object == "job_event"
    assert model.data[0].id == "event123"
    assert model.data[0].type == "training"
    assert model.data[0].created_at == 1617181723
    assert model.data[0].level == "info"
    assert model.data[0].message == "Training has started."
    assert isinstance(model.data[0].data, Metric)
    assert model.data[0].data.epoch == 1
    assert model.data[0].data.current_steps == 100
    assert model.data[0].data.total_steps == 1000
    assert model.data[0].data.elapsed_time == "00:10:00"
    assert model.data[0].data.remaining_time == "05:20:00"
    assert model.data[0].data.trained_tokens == 500000
    assert model.data[0].data.loss == 0.05
    assert model.data[0].data.eval_loss == 0.03
    assert model.data[0].data.acc == 0.9
    assert model.data[0].data.eval_acc == 0.95
    assert model.data[0].data.learning_rate == 0.001
    assert model.has_more == False


@pytest.mark.parametrize(
    "R",
    [
        EmbeddingsResponded

    ],
)
def test_response_embedding_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content="""{
    "object": "embeddings",
    "data": [
      {
        "object": "embedding",
        "index": 1,
        "embedding": [0.1, 0.2] 
      }
    ],
    "model": "some-model-name",
    "usage": {
      "prompt_tokens": 20,
      "completion_tokens": 30,
      "total_tokens": 50
    }
  }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model, EmbeddingsResponded)
    assert isinstance(model.data, list)
    assert isinstance(model.data[0], Embedding)
    assert model.data[0].object == "embedding"
    assert model.data[0].index == 1
    assert model.data[0].embedding == [0.1, 0.2]
    assert model.object == "embeddings"
    assert model.model == "some-model-name"
    assert model.usage.prompt_tokens == 20
    assert model.usage.completion_tokens == 30
    assert model.usage.total_tokens == 50


@pytest.mark.parametrize(
    "R",
    [

        FileObject,

    ],
)
def test_response_file_list_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content=""" {
        "id": "12345",
        "bytes": 1024,
        "created_at": 1617181723,
        "filename": "example.txt",
        "object": "file",
        "purpose": "example purpose",
        "status": "uploaded",
        "status_details": "File uploaded successfully"
      }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model, FileObject)
    assert model.id == "12345"
    assert model.bytes == 1024
    assert model.created_at == 1617181723
    assert model.filename == "example.txt"
    assert model.object == "file"
    assert model.purpose == "example purpose"
    assert model.status == "uploaded"
    assert model.status_details == "File uploaded successfully"


@pytest.mark.parametrize(
    "R",
    [

        ListOfFileObject,

    ],
)
def test_response_file_list_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content="""{
    "object": "list",
    "data": [
      {
        "id": "12345",
        "bytes": 1024,
        "created_at": 1617181723,
        "filename": "example.txt",
        "object": "file",
        "purpose": "example purpose",
        "status": "uploaded",
        "status_details": "File uploaded successfully"
      }
    ],
    "has_more": true
  }"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model.data, list)
    assert isinstance(model.data[0], FileObject)
    assert model.data[0].id == "12345"
    assert model.data[0].bytes == 1024
    assert model.data[0].created_at == 1617181723
    assert model.data[0].filename == "example.txt"
    assert model.data[0].object == "file"
    assert model.data[0].purpose == "example purpose"
    assert model.data[0].status == "uploaded"
    assert model.data[0].status_details == "File uploaded successfully"
    assert model.has_more == True


@pytest.mark.parametrize(
    "R",
    [
        ImagesResponded

    ]
)
def test_response_image_model_cast(
        R: Type[BaseModel]
) -> None:
    MockClient._process_response_data = HttpClient._process_response_data
    response = httpx.Response(
        status_code=200,
        content="""{
"created": 1234567890,
"data": [
  {
    "b64_json": "base64_encoded_string",
    "url": "http://example.com/image.png",
    "revised_prompt": "Revised prompt text"
  }
]
}"""
    )

    http_response = HttpResponse(
        raw_response=response,
        cast_type=R,
        client=MockClient(),
        stream=False,
        stream_cls=None
    )
    model = http_response.parse()

    assert R == model.__class__
    assert isinstance(model.data, list)
    assert isinstance(model.data[0], GeneratedImage)
    assert model.data[0].b64_json == "base64_encoded_string"
