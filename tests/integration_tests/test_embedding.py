from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config


def test_embeddings(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore

    client = ZhipuAI()
    try:
        response = client.embeddings.create(
            model="embedding-2", #填写需要调用的模型名称
            input="你好",
            extra_body={"model_version": "v1"}
        )
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)
