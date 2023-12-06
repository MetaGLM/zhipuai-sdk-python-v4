from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")


completion = client.chat.asyncCompletions.retrieve_completion_result(
    id="",
    # return_json= True,
)

print(completion)
