from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市，如：北京",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    }
]
messages = [{"role": "user", "content": "今天北京天气如何？"}]
completion = client.chat.completions.create(
    model="chatglm3-6b-latest",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    # stream=True,
)
# completion = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         },
#     ],
# )
print(completion.choices)
# for chunk in completion:
#     # if not chunk.choices:
#     #     continue
#     print(chunk)
