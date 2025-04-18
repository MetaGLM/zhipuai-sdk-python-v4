from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config


def test_web_search(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.web_search.web_search(
            search_engine="search-std",
            search_query="2025特朗普向中国加征了多少关税"
        )
        print(response)

    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

