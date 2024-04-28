import os.path

from zhipuai import ZhipuAI
import zhipuai


def test_completions_temp0():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": "tell me a joke"
                }
            ],
            top_p=0.7,
            temperature=0,
            max_tokens=2000,
        )
        print(response)

    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_temp1():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": "tell me a joke"
                }
            ],
            top_p=0.7,
            temperature=1,
            max_tokens=2000,
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_top0():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": "tell me a joke"
                }
            ],
            top_p=0,
            temperature=0.9,
            max_tokens=2000,
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_top1():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": "tell me a joke"
                }
            ],
            top_p=1,
            temperature=0.9,
            max_tokens=2000,
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                {"role": "user", "content": "智谱AI开放平台"},
                {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
                {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "帮我看看清华的升学率",
                        "search_result": True,
                    }
                }
            ],
            extra_body={"temperature": 0.5, "max_tokens": 50},
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_disenable_web_search():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                {"role": "user", "content": "智谱AI开放平台"},
                {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
                {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "帮我看看清华的升学率",
                        "search_result": True,
                        "enable": False,
                    }
                }
            ],
            extra_body={"temperature": 0.5, "max_tokens": 50},
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_enable_web_search():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                {"role": "user", "content": "智谱AI开放平台"},
                {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
                {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "帮我看看清华的升学率",
                        "search_result": True,
                        "enable": True,
                    }
                }
            ],
            extra_body={"temperature": 0.5, "max_tokens": 50},
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_stream():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            stream=True,
            messages=[
                {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                {"role": "user", "content": "智谱AI开放平台"},
                {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
                {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
            ],
            extra_body={"temperature": 0.5, "max_tokens": 50},
        )
        for item in response:
            print(item)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


# Function to encode the image
def encode_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def test_completions_vis():
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.chat.completions.create(
            model="glm-4v",  # 填写需要调用的模型名称
            extra_body={"temperature": 0.5, "max_tokens": 50},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "图里有什么"
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
                            }
                        }
                    ]
                }
            ]
        )
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_completions_vis_base64(test_file_path):
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        base64_image = encode_image(os.path.join(test_file_path, "img/MetaGLM.png"))
        response = client.chat.completions.create(
            model="glm-4v",  # 填写需要调用的模型名称
            extra_body={"temperature": 0.5, "max_tokens": 50},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "图里有什么"
                        },

                        # {
                        #     "type": "image_url",
                        #     "image_url": {
                        #         "url": "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
                        #     }
                        # },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_async_completions():
    client = ZhipuAI()  # 请填写您自己的APIKey
    try:
        response = client.chat.asyncCompletions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                {"role": "user", "content": "智谱AI开放平台"},
                {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
                {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "帮我看看清华的升学率",
                        "search_result": True,
                    }
                }
            ],
            extra_body={"temperature": 0.5, "max_tokens": 50},
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_retrieve_completion_result():
    client = ZhipuAI()  # 请填写您自己的APIKey
    try:
        response = client.chat.asyncCompletions.retrieve_completion_result(id="1014908592669352541651237")
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


if __name__ == '__main__':
    test_completions_enable_web_search()
