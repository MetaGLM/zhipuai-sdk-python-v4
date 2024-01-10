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
    model="", #填写需要调用的模型名称
    messages=messages,
    tools=tools,
    tool_choice="auto",
    stream=True
)

for chunk in completion:
    print(chunk)
