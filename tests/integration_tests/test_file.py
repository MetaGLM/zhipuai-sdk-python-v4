from zhipuai import ZhipuAI
import zhipuai
import os


def test_files(test_file_path):
    client = ZhipuAI()
    try:
        result = client.files.create(
            file=open(os.path.join(test_file_path,"demo.jsonl"), "rb"),
            purpose="fine-tune"
        )
        print(result)
        # "file-20240418025911536-6dqgr"


    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)


def test_files_validation(test_file_path):
    client = ZhipuAI()
    try:
        result = client.files.create(
            file=open(os.path.join(test_file_path,"demo.jsonl"), "rb"),
            purpose="fine-tune"
        )
        print(result)
        # "file-20240418025931214-c87tj"



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

def test_files_list():
    client = ZhipuAI()
    try:
        list = client.files.list()
        print(list)



    except zhipuai.core._errors.APIRequestFailedError as err:
        print(err)
    except zhipuai.core._errors.APIInternalError as err:
        print(err)
    except zhipuai.core._errors.APIStatusError as err:
        print(err)

if __name__ == "__main__":
    test_files_list()