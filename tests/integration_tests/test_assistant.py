import os
import logging
import logging.config
import zhipuai
from zhipuai import ZhipuAI


def test_assistant(logging_conf) -> None:


    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    generate = client.assistant.conversation(
        assistant_id="659e54b1b8006379b4b2abd6",
        model="GLM-4-Assistant",
        messages=[
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "帮我搜索下智谱的cogvideox发布时间"
                }
            }
        ],
        stream=True,
        attachments=None,
        metadata=None,
        request_id="request_1790291013237211136",
        user_id="12345678"
    )
    for assistant in generate:
        print(assistant)

