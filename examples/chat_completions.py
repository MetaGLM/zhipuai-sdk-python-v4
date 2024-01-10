from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")

response = client.chat.completions.create(
    model="",  # 填写需要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个人工智能助手，你叫叫chatGLM"},
        {"role": "user", "content": "你好！你叫什么名字"},
    ],
    # top_p=0.7,
    # temperature=0.9,
    stream=True,
)

for chunk in response:
    print(chunk.choices[0].delta)
