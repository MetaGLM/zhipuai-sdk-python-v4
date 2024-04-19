from zhipuai import ZhipuAI


def test_finetuning_create():
    client = ZhipuAI()  # 请填写您自己的APIKey

    job = client.fine_tuning.jobs.create(
        model="chatglm3-6b",
        training_file="file-20240418025931214-c87tj",  # 请填写已成功上传的文件id
        validation_file="file-20240418025931214-c87tj",  # 请填写已成功上传的文件id
        suffix="demo_test",
    )
    job_id = job.id
    print(job_id)
    fine_tuning_job = client.fine_tuning.jobs.retrieve(fine_tuning_job_id=job_id)
    print(fine_tuning_job)
    #     ftjob-20240418110039323-j8lh2


def test_finetuning_retrieve():
    client = ZhipuAI()  # 请填写您自己的APIKey

    fine_tuning_job = client.fine_tuning.jobs.retrieve(fine_tuning_job_id="ftjob-20240418110039323-j8lh2")
    print(fine_tuning_job)


def test_finetuning_job_list():
    client = ZhipuAI()  # 请填写您自己的APIKey
    job_list = client.fine_tuning.jobs.list()

    print(job_list)


def test_model_check():
    client = ZhipuAI()  # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="chatglm3-6b-8572905046912426020-demo_test",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "你是一位乐于助人，知识渊博的全能AI助手。"},
            {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
        ],
        extra_body={"temperature": 0.5, "max_tokens": 50},
    )
    print(response.choices[0].message)


if __name__ == "__main__":
    test_model_check()
