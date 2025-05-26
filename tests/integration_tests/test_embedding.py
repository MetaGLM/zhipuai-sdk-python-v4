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


def test_embeddings_dimensions(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore

    client = ZhipuAI()
    try:
        response = client.embeddings.create(
            model="embedding-3", #填写需要调用的模型名称
            input="你好",
            dimensions=512,
            extra_body={"model_version": "v1"}
        )
        assert response.data[0].object == "embedding"
        assert len(response.data[0].embedding) == 512
        print(len(response.data[0].embedding))


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)
