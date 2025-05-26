# -*- coding: utf-8 -*-

from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config


def test_completions_emohaa(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 请填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="emohaa",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "assistant",
                    "content": "你好，我是Emohaa，很高兴见到你。请问有什么我可以帮忙的吗？"
                },
                {
                    "role": "user",
                    "content": "今天我休息，决定去西安保密逛逛，心情很好地喷上了我最爱的烟熏木制香"
                },
                {
                    "role": "assistant",
                    "content": "今天我休息，决定去西安保密逛逛，心情很好地喷上了我最爱的烟熏木制香"
                }
            ],
            meta={
                "user_info": "30岁的男性软件工程师，兴趣包括阅读、徒步和编程",
                "bot_info": "Emohaa是一款基于Hill助人理论的情感支持AI，拥有专业的心理咨询话术能力",
                "bot_name": "Emohaa",
                "user_name": "陆星辰"
            },
        )
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

