
def test_sdk_import():
    from zhipuai import ZhipuAI

    client = ZhipuAI()  # 请填写您自己的APIKey

    if client is not None:
        print("SDK导入成功")
    else:
        print("SDK导入失败")