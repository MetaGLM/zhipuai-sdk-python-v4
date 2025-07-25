def test_audio_error_field():
    from zhipuai.types.audio.audio_speech_chunk import AudioSpeechChunk, AudioError, AudioSpeechChoice, AudioSpeechDelta

    # 构造一个 AudioError
    error = AudioError(code="500", message="Internal Error")

    # 构造一个完整的 AudioSpeechChunk
    chunk = AudioSpeechChunk(
        choices=[
            AudioSpeechChoice(
                delta=AudioSpeechDelta(content="audio", role="system"),
                finish_reason="error",
                index=0
            )
        ],
        request_id="req_2",
        created=123456,
        error=error
    )

    # 检查 error 字段是否为 AudioError 实例
    assert isinstance(chunk.error, AudioError)
    assert chunk.error.code == "500"
    assert chunk.error.message == "Internal Error"

    # 检查序列化
    as_dict = chunk.model_dump()
    assert as_dict["error"]["code"] == "500"
    assert as_dict["error"]["message"] == "Internal Error"
    print("test_audio_error_field passed.")
