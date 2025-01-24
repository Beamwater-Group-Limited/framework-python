import json

import requests
from prefect import task

from app.model.come_entity import ComeEntity
from app.model.context_entity import ContextEntity
from app.model.data_item import DataItem, DaType, DaFormat
from app.model.prefect_run.req_parameter import ReqParameter, DataItemRealData
from app.prompts import llava_prompts


class TaskNode:
    def __init__(self, task_name, http_url: str, come: [], go: [], is_last: bool):
        self.task_name = task_name
        self.http_url = http_url
        self.come = come
        self.go = go
        self.is_last = is_last

    @task()
    def run(self, param_data):
        # 根据come，替换掉其中需要传入的值
        new_come = self.update_param_come(param_data)

        cheng_schema = llava_prompts.cheng_schema
        comeEntity = ComeEntity().setup(comes=new_come, context=ContextEntity())

        # 定义 JSON 数据
        payload = comeEntity.obj2dct()
        # 发送 POST 请求
        headers = {"Content-Type": "application/json"}
        print(payload)
        response = requests.post(self.http_url, json=payload, headers=headers)
        hao_comeEntity = ComeEntity.as_ComeEntity(response.json())

        print(hao_comeEntity.obj2dct())

        if self.is_last:
            param_data = self.add_return_come_to_param_last(hao_comeEntity.comes, param_data)
        else:
            # 更新param_data
            param_data = self.add_return_come_to_param(hao_comeEntity.comes, param_data)

        return param_data

    # 修改come的值，为其中需要传入的内容，放入真实数据
    def update_param_come(self, param_data: ReqParameter):
        new_come = []
        for item in self.come:
            """
            遍历come，判断当前的DataItem，是否需要传入真实的值
            """
            flag = False
            for pp in param_data.gs_input_data + param_data.process_param_data:
                if pp.data_type == item["type"] and pp.data_format == item["format"] and pp.content == item[
                                  "content"]:
                    new_come.append(DataItem(DaType(item["type"]), DaFormat(item["format"]), pp.data))
                    flag = True
                    break

            if not flag:
                new_come.append(DataItem(DaType(item["type"]), DaFormat(item["format"]), item["content"]))
        return new_come

    # 修改come的值，将返回值填入到process_param中
    def add_return_come_to_param(self, return_come: [], param_data: ReqParameter):
        for index, item in enumerate(self.go):
            return_item = return_come[index]
            single_process_param_data = DataItemRealData(DaType(item["type"]), DaFormat(item["format"]), item["content"],
                                                         return_item.content)
            param_data.process_param_data.append(single_process_param_data)
        return param_data

    # 调用最后一个任务时
    # 修改come的值，将返回值填入到gs_output_data中
    def add_return_come_to_param_last(self, return_come: [], param_data: ReqParameter):
        for index, item in enumerate(self.go):
            return_item = return_come[index]
            for output_data in param_data.gs_output_data:
                if output_data.data_type == item["type"] and output_data.data_format == item["format"]:
                    output_data.content = return_item.content
                    break
        return param_data
