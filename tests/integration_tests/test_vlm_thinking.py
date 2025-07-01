import os.path

from zhipuai import ZhipuAI
import zhipuai
import time

import logging
import logging.config


def test_completions_vlm_thinking(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        # 生成request_id
        request_id = time.time()
        print(f"request_id:{request_id}")
        response = client.chat.completions.create(
            request_id=request_id,
            model="glm-4.1v-thinking-flash",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "图里有什么"
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
                            }
                        }
                    ]
                }
            ],
            temperature=0.5,
            max_tokens = 1024,
            user_id="12345678"
        )
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)



def test_completions_vlm_thinking_stream(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        # 生成request_id
        request_id = time.time()
        print(f"request_id:{request_id}")
        response = client.chat.completions.create(
            request_id=request_id,
            model="glm-4.1v-thinking-flash",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "图里有什么"
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
                            }
                        }
                    ]
                }
            ],
            temperature=0.5,
            max_tokens = 1024,
            user_id="12345678",
            stream=True
        )
        for item in response:
            print(item)

    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

