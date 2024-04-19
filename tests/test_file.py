from zhipuai import ZhipuAI


def test_files():
    client = ZhipuAI()
    result = client.files.create(
        file=open("/jfs/chat/zhipu/finetuning/demo.jsonl", "rb"),
        purpose="fine-tune"
    )
    print(result)
    # "file-20240418025911536-6dqgr"


def test_files_validation():
    client = ZhipuAI()
    result = client.files.create(
        file=open("/jfs/chat/zhipu/finetuning/demo.jsonl", "rb"),
        purpose="fine-tune"
    )
    print(result)
    # "file-20240418025931214-c87tj"


def test_files_list():
    client = ZhipuAI()

    list = client.files.list()
    print(list)


if __name__ == "__main__":
    test_files_list()
