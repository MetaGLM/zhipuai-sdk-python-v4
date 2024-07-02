import os.path

from zhipuai import ZhipuAI
import zhipuai
import time

import logging
import logging.config


def test_code_geex(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        # 生成request_id
        request_id = time.time()
        print(f"request_id:{request_id}")
        response = client.chat.completions.create(
            request_id=request_id,
            model="codegeex-4",
            messages=[
                {
                    "role": "system",
                    "content": """你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。
                    任务：请为输入代码提供格式规范的注释，包含多行注释和单行注释，请注意不要改动原始代码，只需要添加注释。 
                    请用中文回答。"""
                },
                {
                    "role": "user",
                    "content": """写一个快速排序函数"""
                }
            ],
            top_p=0.7,
            temperature=0.9,
            max_tokens=2000,
            stop=["<|endoftext|>", "<|user|>", "<|assistant|>", "<|observation|>"],
            code_geex_extra={
                "target": {
                    "path": "11111",
                    "language": "Python",
                    "code_prefix": "EventSource.Factory factory = EventSources.createFactory(OkHttpUtils.getInstance());",
                    "code_suffix": "TaskMonitorLocal taskMonitorLocal = getTaskMonitorLocal(algoMqReq);"
                },
                "contexts": [
                    {
                        "path": "/1/2",
                        "code": "if(!sensitiveUser){ZpTraceUtils.addAsyncAttribute(algoMqReq.getTaskOrderNo(), ApiTraceProperty.request_params.getCode(), modelSendMap);"
                    }

                ]
            }
        )
        print(response)

    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)
