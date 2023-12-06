# import os
#
# from .model_api import model_api
#
# api_key = os.environ.get(API_KEY)
#
# api_timeout_seconds = 300
#
# model_api_url = os.environ.get(
#     ZHIPUAI_MODEL_API_URL, https://open.bigmodel.cn/api/paas/v3/model-api
# )

from ._client import ZhipuAI

from .core._errors import (
    ZhipuAIError,
    APIStatusError,
    APIRequestFailedError,
    APIAuthenticationError,
    APIReachLimitError,
    APIInternalError,
    APIServerFlowExceedError,
    APIResponseError,
    APIResponseValidationError,
    APITimeoutError,
)
