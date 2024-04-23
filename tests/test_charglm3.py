from zhipuai import ZhipuAI
import zhipuai


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


def test_async_completions():
    client = ZhipuAI()  # 请填写您自己的APIKey
    response = client.chat.asyncCompletions.create(
        model="charglm",  # 填写需要调用的模型名称
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


def test_retrieve_completion_result():
    client = ZhipuAI()  # 请填写您自己的APIKey
    response = client.chat.asyncCompletions.retrieve_completion_result(id="1014908592669352541650991")
    print(response)


if __name__ == "__main__":
    test_completions_charglm()
