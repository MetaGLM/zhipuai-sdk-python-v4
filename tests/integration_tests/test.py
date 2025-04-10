# import time
#
# from zhipuai import ZhipuAI
# client = ZhipuAI()  # 填写您自己的APIKey
#
# response = client.videos.generations(
#     model="cogvideo",
#     prompt="一个年轻的艺术家在一片彩虹上用调色板作画。"
#     # prompt="一只卡通狐狸在森林里跳着欢快的爵士舞。"
#     # prompt="这是一部汽车广告片，描述了一位30岁的汽车赛车手戴着红色头盔的赛车冒险。背景是蔚蓝的天空和苛刻的沙漠环境，电影风格使用35毫米胶片拍摄，色彩鲜艳夺目。"
# )
# print(response)
# task_id = response.id
# task_status = response.task_status
# get_cnt = 0
#
# while task_status == 'PROCESSING' and get_cnt <= 40:
#     result_response = client.videos.retrieve_videos_result(
#         id=task_id
#     )
#     print(result_response)
#     task_status = result_response.task_status
#
#     time.sleep(2)
#     get_cnt += 1
