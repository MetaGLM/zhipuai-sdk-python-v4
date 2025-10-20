Z.AI 和 智谱AI 的 [全新 Python SDK](https://github.com/zai-org/z-ai-sdk-python) 已经发布：[z-ai-sdk-python](https://github.com/zai-org/z-ai-sdk-python)！推荐使用此 SDK，以获得更好、更快的长期支持。


# 智谱AI开放平台 Python SDK

[![PyPI version](https://img.shields.io/pypi/v/zhipuai.svg)](https://pypi.org/project/zhipuai/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

[English Readme](README.md)

[智谱AI开放平台](https://open.bigmodel.cn/dev/api)官方 Python SDK，帮助开发者快速集成智谱AI强大的人工智能能力到Python应用中。

## ✨ 特性

- 🚀 **类型安全**: 所有接口完全类型封装，无需查阅API文档即可完成接入
- 🔧 **简单易用**: 简洁直观的API设计，快速上手
- ⚡ **高性能**: 基于现代Python库构建，性能优异
- 🛡️ **安全可靠**: 内置身份验证和令牌管理
- 📦 **轻量级**: 最小化依赖，易于项目集成
- 🔄 **流式支持**: 支持SSE流式响应和异步调用

## 📦 安装

### 环境要求
- Python 3.9 或更高版本
- pip 包管理器

### 使用 pip 安装

```sh
pip install zhipuai
```

### 📋 核心依赖

本SDK使用以下核心依赖库：

| 依赖库 | 用途 |
|--------|------|
| httpx | HTTP客户端库 |
| pydantic | 数据验证和序列化 |
| typing-extensions | 类型注解扩展 |

## 🚀 快速开始

### 基本用法

1. **使用API密钥创建客户端**
2. **调用相应的API方法**

完整示例请参考开放平台[接口文档](https://open.bigmodel.cn/dev/api)以及[使用指南](https://open.bigmodel.cn/dev/howuse/)，记得替换为您自己的API密钥。

### 客户端配置

SDK支持多种方式配置API密钥：

**环境变量配置：**
```bash
export ZHIPUAI_API_KEY="your_api_key_here"
export ZHIPUAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"  # 可选
```

**代码配置：**
```python
from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key="your_api_key_here",  # 填写您的 APIKey
) 
```
**高级配置：**

SDK提供了灵活的客户端配置选项：

```python
import httpx
from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key="your_api_key_here",
    timeout=httpx.Timeout(timeout=300.0, connect=8.0),  # 超时配置
    max_retries=3,  # 重试次数
    base_url="https://open.bigmodel.cn/api/paas/v4/"  # Custom API endpoint
)
```

**配置选项：**
- `timeout`: 控制接口连接和读取超时时间
- `max_retries`: 控制重试次数，默认为3次
- `base_url`: 自定义API基础URL


## 💡 使用示例

### 基础对话

```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好，请介绍一下智谱AI"}
    ],
    tools=[
        {
            "type": "web_search",
            "web_search": {
                "search_query": "Search the Zhipu",
                "search_result": True,
            }
        }
    ],
    extra_body={"temperature": 0.5, "max_tokens": 50}
)
print(response.choices[0].message.content)
```

### 流式对话

```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个人工智能助手，你叫ChatGLM"},
        {"role": "user", "content": "你好！你叫什么名字"},
    ],
    stream=True,
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta)
```

### 多模态对话

```python
import base64
from zhipuai import ZhipuAI

def encode_image(image_path):
    """将图片编码为base64格式"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = ZhipuAI()  # 请填写您自己的APIKey
base64_image = encode_image("path/to/your/image.jpg")

response = client.chat.completions.create(
    model="glm-4v",  # 视觉模型
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请描述这张图片的内容"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    extra_body={"temperature": 0.5, "max_tokens": 50}
)
print(response.choices[0].message.content)
```

### 角色扮演

```python
from zhipuai import ZhipuAI

client = ZhipuAI()  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="charglm-3",  # 角色扮演模型
    messages=[
        {
            "role": "user",
            "content": "你好，最近在忙什么呢？"
        }
    ],
    meta={
        "user_info": "我是一位电影导演，擅长拍摄音乐题材的电影。",
        "bot_info": "你是一位当红的国内女歌手及演员，拥有出众的音乐才华。",
        "bot_name": "小雅",
        "user_name": "导演"
    },
)
print(response.choices[0].message.content)
```

### 智能体对话

```python
from zhipuai import ZhipuAI

client = ZhipuAI()  # 请填写您自己的APIKey

response = client.assistant.conversation(
    assistant_id="your_assistant_id",  # 智能体ID，可用 65940acff94777010aa6b796 进行测试
    model="glm-4-assistant",
    messages=[
        {
            "role": "user",
            "content": [{
                "type": "text",
                "text": "帮我搜索智谱AI的最新产品信息"
            }]
        }
    ],
    stream=True,
    attachments=None,
    metadata=None,
    request_id="request_1790291013237211136",
    user_id="12345678"
)

for chunk in response:
    print(chunk)
```

### 视频生成

```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")
response = client.videos.generations(
    model="cogvideox-2",
    prompt="一个美丽的日落海滩场景",   # 生成内容的提示词
    quality="quality",          # 输出模式：'quality' 表示质量优先，'speed' 表示速度优先
    with_audio=True,            # 生成带背景音频的视频
    size="1920x1080",           # 视频分辨率（最高支持 4K，例如 "3840x2160"）
    fps=30,                     # 帧率（可选 30 或 60）
    user_id="user_12345"
)

# 生成过程可能需要一些时间
result = client.videos.retrieve_videos_result(id=response.id)
print(result)
```

## 🚨 异常处理

SDK提供了完善的异常处理机制：

```python
from zhipuai import ZhipuAI
import zhipuai

client = ZhipuAI()  # 请填写您自己的APIKey

try:
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "user", "content": "你好，智谱AI！"}
        ]
    )
    print(response.choices[0].message.content)
    
except zhipuai.APIStatusError as err:
    print(f"API状态错误: {err}")
except zhipuai.APITimeoutError as err:
    print(f"请求超时: {err}")
except Exception as err:
    print(f"其他错误: {err}")
```

### 错误码说明

| 状态码 | 错误类型 | 说明 |
|--------|----------|------|
| 400 | `APIRequestFailedError` | 请求参数错误 |
| 401 | `APIAuthenticationError` | 身份验证失败 |
| 429 | `APIReachLimitError` | 请求频率超限 |
| 500 | `APIInternalError` | 服务器内部错误 |
| 503 | `APIServerFlowExceedError` | 服务器流量超限 |
| N/A | `APIStatusError` | 通用API错误 |

## 📈 版本更新

详细的版本更新记录和历史信息，请查看 [Release-Note.md](Release-Note.md)。

## 📄 许可证

本项目基于 MIT 许可证开源 - 详情请查看 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎贡献代码！请随时提交 Pull Request。

## 📞 支持

如有问题和技术支持，请访问 [智谱AI开放平台](https://open.bigmodel.cn/) 或查看我们的文档。
  
