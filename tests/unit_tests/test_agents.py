def test_agents_completion_error_field():
    from zhipuai.types.agents.agents_completion import AgentsCompletion, AgentsError, AgentsCompletionChoice, AgentsCompletionMessage, AgentsCompletionUsage

    # 构造一个 AgentsError
    error = AgentsError(code="404", message="Not Found")

    # 构造一个完整的 AgentsCompletion
    completion = AgentsCompletion(
        agent_id="test_agent",
        conversation_id="conv_1",
        status="failed",
        choices=[
            AgentsCompletionChoice(
                index=0,
                finish_reason="error",
                message=AgentsCompletionMessage(content="error", role="system")
            )
        ],
        request_id="req_1",
        id="id_1",
        usage=AgentsCompletionUsage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
        error=error
    )

    # 检查 error 字段是否为 AgentsError 实例
    assert isinstance(completion.error, AgentsError)
    assert completion.error.code == "404"
    assert completion.error.message == "Not Found"

    # 检查序列化
    as_dict = completion.model_dump()
    assert as_dict["error"]["code"] == "404"
    assert as_dict["error"]["message"] == "Not Found"
    print("test_agents_completion_error_field passed.")