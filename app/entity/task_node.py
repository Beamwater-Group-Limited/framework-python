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

    def add_parameters(self, kwargs: dict):
        for item in self.parameters:
            if item.get("is_update") == "0":
                k = item.get("key")
                v = item.get("default_value")
                kwargs[k] = v
        return kwargs
