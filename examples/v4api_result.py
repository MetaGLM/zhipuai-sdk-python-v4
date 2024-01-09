from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")

completion = client.chat.asyncCompletions.retrieve_completion_result(
    id="531516957209486438181245467268350215",
    disable_strict_validation=True,
)

print(completion)
