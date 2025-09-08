from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config

def test_mcp_tool_server_url_sse(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()
    messages = [
        {"role": "user", "content": "今天是几月几号？"}
    ]
    try:
        response = client.chat.completions.create(
            model="glm-4",
            stream=False,
            messages=messages,
            tools=[
                {
                    "type": "mcp",
                    "mcp": {
                        "headers": {"Authorization": ""}, # 替换成用户的 header
                        "server_label": "sougou_search",
                        "transport_type": "sse",
                        "server_url": "https://open.bigmodel.cn/api/mcp/sogou/sse"
                    }
                },
            ]
        )
        print(response)
    except Exception as err:
        print(err)

def test_mcp_tool_server_label(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()
    messages = [
        {"role": "user", "content": "北京现在天气怎么样？"}
    ]
    try:
        response = client.chat.completions.create(
            model="glm-4",
            stream=True,
            messages=messages,
            tools=[
                {
                    "type": "mcp",
                    "mcp": {
                        "headers": {"Authorization": ""}, # 替换成用户的 header
                        "server_label": "aviation",
                    }
                },
            ]
        )
        for item in response:
            print(item)
    except Exception as err:
        print(err)