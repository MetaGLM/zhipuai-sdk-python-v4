from __future__ import annotations

import unittest
import os

import logging
import logging.config

import zhipuai

import httpx
import pytest
from respx import MockRouter

from zhipuai import ZhipuAI
from zhipuai.api_resource import FilesWithRawResponse


@pytest.fixture(scope='class')
def test_server():
    class SharedData:
        client = ZhipuAI()
        file_id1 = None
        file_id2 = None

    return SharedData()


class TestZhipuAIFileServer:

    def test_logs(self, logging_conf):
        logging.config.dictConfig(logging_conf)  # type: ignore

    def test_files(self, test_server, test_file_path):

        try:
            result = test_server.client.files.create(
                file=open(os.path.join(test_file_path, "demo.jsonl"), "rb"),
                purpose="fine-tune"
            )
            print(result)
            test_server.file_id1 = result.id


        except zhipuai.core._errors.APIRequestFailedError as err:
            print(err)
        except zhipuai.core._errors.APIInternalError as err:
            print(err)
        except zhipuai.core._errors.APIStatusError as err:
            print(err)

    def test_files_validation(self, test_server, test_file_path):
        try:
            result = test_server.client.files.create(
                file=open(os.path.join(test_file_path, "demo.jsonl"), "rb"),
                purpose="fine-tune"
            )
            print(result)

            test_server.file_id2 = result.id



        except zhipuai.core._errors.APIRequestFailedError as err:
            print(err)
        except zhipuai.core._errors.APIInternalError as err:
            print(err)
        except zhipuai.core._errors.APIStatusError as err:
            print(err)

    def test_files_list(self, test_server):
        try:
            list = test_server.client.files.list()
            print(list)



        except zhipuai.core._errors.APIRequestFailedError as err:
            print(err)
        except zhipuai.core._errors.APIInternalError as err:
            print(err)
        except zhipuai.core._errors.APIStatusError as err:
            print(err)

    def test_delete_files(self, test_server):
        try:
            delete1 = test_server.client.files.delete(
                file_id=test_server.file_id1
            )
            print(delete1)

            delete2 = test_server.client.files.delete(
                file_id=test_server.file_id2
            )
            print(delete2)



        except zhipuai.core._errors.APIRequestFailedError as err:
            print(err)
        except zhipuai.core._errors.APIInternalError as err:
            print(err)
        except zhipuai.core._errors.APIStatusError as err:
            print(err)
