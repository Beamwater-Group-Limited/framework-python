from prefect import task
import requests
import json


class TaskNode:
    def __init__(self, task_name, http_url: str, parameters, come: [], go: []):
        self.task_name = task_name
        self.http_url = http_url
        self.come = come
        self.go = go
        self.parameters = parameters

    @task()
    def run(self, kwargs: dict) -> dict:
        # 获取这个方法需要的参数
        kwargs = self.add_parameters(kwargs)
        # 判断是否包含图像上传 -- 取消使用
        # if kwargs["image_data"] is not None or kwargs["image_data"] != "":
        #     image_input = self.upload_img(kwargs["image_data"])
        #     kwargs["image_data"] = image_input
        # 调用请求，并传值
        response = requests.post(self.http_url, data=kwargs)
        json_string = response.content.decode('utf-8')
        # 将字符串解析为 JSON 对象
        json_data = json.loads(json_string)
        back = json_data['data']

        kwargs = self.update_kwargs(back, kwargs)

        return kwargs

    # 修改中间值的状态
    def update_kwargs(self, request_back, kwargs: dict):
        kwargs.update(request_back)
        return kwargs

    # def upload_img(self, img_data):
    #     response = requests.post("http://192.168.0.70:8080/v1/save_img_data", data={"file": img_data})
    #     json_string = response.content.decode('utf-8')
    #     # 将字符串解析为 JSON 对象
    #     json_data = json.loads(json_string)
    #     back = json_data['data']
    #     return back

    def add_parameters(self, kwargs: dict):
        for item in self.parameters:
            if str(item.get("is_update")) == "0":
                k = item.get("key")
                v = item.get("default_value")
                kwargs[k] = v
        return kwargs
