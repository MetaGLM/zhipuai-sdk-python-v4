# 智谱大模型开放接口SDK

[![PyPI version](https://img.shields.io/pypi/v/zhipuai.svg)](https://pypi.org/project/zhipuai/)

智谱[开放平台](https://open.bigmodel.cn/dev/api)大模型接口 Python SDK（Big Model API SDK in Python），让开发者更便捷的调用智谱开放API


## 简介
- 对所有接口进行了类型封装。
- 初始化client并调用成员函数，无需关注http调用过程的各种细节，所见即所得。
- 默认缓存token。

## 安装


- 运行环境： [**Python>=3.7**](https://www.python.org/)

- 使用 pip 安装 `zhipuai` 软件包及其依赖

```sh
pip install zhipuai
```

## 使用

- 调用流程：
    1. 使用 APISecretKey 创建 Client
    2. 调用 Client 对应的成员方法
- 开放平台[接口文档](https://open.bigmodel.cn/dev/api)以及[使用指南](https://open.bigmodel.cn/dev/howuse/)中有更多的 demo 示例，请在 demo 中使用自己的 ApiKey 进行测试。

### 创建Client
sdk支持通过环境变量配置APIKey
- env

`ZHIPUAI_API_KEY`: 您的APIKey

`ZHIPUAI_BASE_URL`: 您的API地址

- 也支持通过代码传入APIKey
```python
from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key="", # 填写您的 APIKey
) 
```

### 同步调用

```python
from zhipuai import ZhipuAI 
 
client = ZhipuAI()  # 填写您自己的APIKey
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
  # 拓展参数
  extra_body={"temperature": 0.5, "max_tokens": 50},
)
print(response) 
```

### SSE 调用

```python
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="") # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="",  # 填写需要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个人工智能助手，你叫叫chatGLM"},
        {"role": "user", "content": "你好！你叫什么名字"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)
```

### 多模态
```python


# Function to encode the image
def encode_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def test_completions_vis():
  client = ZhipuAI()  # 填写您自己的APIKey
  base64_image  = encode_image("img/MetaGLM.png")
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

test_completions_vis()
```

### 角色扮演
> 提供能力的模型名称，请从官网获取
```python

def test_completions_charglm():
    client = ZhipuAI()  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="charglm-3",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": "请问你在做什么"
            }
        ],
        extra_body={
            "meta": {
                "user_info": "我是陆星辰，是一个男性，是一位知名导演，也是苏梦远的合作导演。我擅长拍摄音乐题材的电影。苏梦远对我的态度是尊敬的，并视我为良师益友。",
                "bot_info": "苏梦远，本名苏远心，是一位当红的国内女歌手及演员。在参加选秀节目后，凭借独特的嗓音及出众的舞台魅力迅速成名，进入娱乐圈。她外表美丽动人，但真正的魅力在于她的才华和勤奋。苏梦远是音乐学院毕业的优秀生，善于创作，拥有多首热门原创歌曲。除了音乐方面的成就，她还热衷于慈善事业，积极参加公益活动，用实际行动传递正能量。在工作中，她对待工作非常敬业，拍戏时总是全身心投入角色，赢得了业内人士的赞誉和粉丝的喜爱。虽然在娱乐圈，但她始终保持低调、谦逊的态度，深得同行尊重。在表达时，苏梦远喜欢使用“我们”和“一起”，强调团队精神。",
                "bot_name": "苏梦远",
                "user_name": "陆星辰"
            },
        }
    )
    print(response)
test_completions_charglm()
```



### 异常处理

When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of `openai.APIConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of `openai.APIStatusError` is raised, containing `status_code` and `response` properties.

All errors inherit from `openai.APIError`.

```python
import openai
from openai import OpenAI

client = OpenAI()

try:
    client.fine_tunes.create(
        training_file="file-XGinujblHPwGLSztz8cPS8XY",
    )
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |



### 更新日志

`2024-4-23` 
- 一些兼容 `pydantic<3,>=1.9.0 ` 的代码，
- 报文处理的业务请求参数和响应参数可通过配置扩充
- 兼容了一些参数 `top_p:1`,`temperture:0`(do_sample重写false，参数top_p temperture不生效)
- 图像理解部分，  image_url参数base64内容包含 `data:image/jpeg;base64`兼容
- 删除jwt认证逻辑
  