from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")


response = client.chat.asyncCompletions.create(
    model="chatglm3-6b-latest",
    messages=[
        {"role": "user",
         "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"}],
    # top_p=0.7,
    # temperature=0.9,
    return_json=True,
)

print(response)
# for line in response.response.iter_lines():
#     print(line)
# for chunk in response:
#     # if not chunk.choices:
#     #     continue
#     print(chunk)
#