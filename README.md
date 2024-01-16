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

```python
from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key="", # 填写您的 APIKey
) 
```

### 同步调用

```python
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我是人工智能助手"},
        {"role": "user", "content": "你叫什么名字"},
        {"role": "assistant", "content": "我叫chatGLM"},
        {"role": "user", "content": "你都可以做些什么事"}
    ],
)
print(response.choices[0].message)
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

