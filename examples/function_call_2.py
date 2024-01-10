from zhipuai import ZhipuAI

client = ZhipuAI(api_key="", )

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_train_info",
            "description": "根据用户提供的信息，查询对应的车次",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure": {
                        "type": "string",
                        "description": "出发城市或车站",
                    },
                    "destination": {
                        "type": "string",
                        "description": "目的地城市或车站",
                    },
                    "date": {
                        "type": "string",
                        "description": "要查询的车次日期",
                    },
                },
                "required": ["departure", "destination", "date"],
            },
        }
    }
]
messages = [
    {
        "role": "user",
        "content": "你能帮我查询2024年1月1日从北京南站到上海的火车票吗？"
    }
]
response = client.chat.completions.create(
    model="",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    # stream=True,
)

print(response)

