from zhipuai import ZhipuAI


def test_images():
    client = ZhipuAI()  # 填写您自己的APIKey
    response = client.images.generations(
        model="cogview-3", #填写需要调用的模型名称
        prompt="一只可爱的小猫咪",
        extra_body={"user_id": "1222212"},
    )
    print(response)


if __name__ == "__main__":
    test_images()
