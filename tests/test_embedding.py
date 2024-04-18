from zhipuai import ZhipuAI


def test_embeddings():

    client = ZhipuAI()
    response = client.embeddings.create(
        model="embedding-2", #填写需要调用的模型名称
        input="你好",
        extra_body={"model_version": "v1"}
    )
    print(response)


if __name__ == "__main__":
    test_embeddings()
