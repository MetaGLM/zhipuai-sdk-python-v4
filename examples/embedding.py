from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")



response = client.embeddings.create(
    model="", #填写需要调用的模型名称
    input="你好",
    disable_strict_validation=True
)
print(response)
