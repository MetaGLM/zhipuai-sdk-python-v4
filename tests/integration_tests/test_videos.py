from zhipuai import ZhipuAI
import zhipuai

import logging
import logging.config


def test_videos(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.videos.generations(
            model="cogvideo",
            prompt="一个开船的人",

            user_id="1212222"
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_videos_image_url(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.videos.generations(
            model="cogvideo",
            image_url="https://cdn.bigmodel.cn/static/platform/images/solutions/car/empowerment/icon-metric.png",
            prompt="一些相信光的人，举着奥特曼",
            user_id="12222211"
        )
        print(response)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_retrieve_videos_result(logging_conf):
    logging.config.dictConfig(logging_conf)  # type: ignore
    client = ZhipuAI()  # 填写您自己的APIKey
    try:
        response = client.videos.retrieve_videos_result(
            id="1014908869548405238276203"
        )
        print(response)


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)
