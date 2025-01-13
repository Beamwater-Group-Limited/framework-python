# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : prefect_seria
# @File          : prefect_service.py
# @Author        : Yuan
# @Time          : 2024/10/11 16:35
# @Function      : 
# @Desc          :
import yaml
# 动态生成多个任务
from prefect import flow

from app.entity.task_node import TaskNode


class PrefectService:
    def __init__(self, flow_name: str, **kwargs) -> None:
        self.task_list = []
        self.flow_name = flow_name
        self.kwargs = kwargs

    # 流附加任务
    def append_task(self, task) -> None:
        self.task_list.append(task)

    # 执行流
    @flow(log_prints=True)
    def run(self) -> str:
        # 循环调用task执行
        for task in self.task_list:
            print(f"当前处理的任务为{task.task_name}")
            self.kwargs = task.run(self.kwargs)
        return self.kwargs


class PrefectDealService:
    def parse_flow_yaml(self, yaml_path):
        with open(yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)
        return existing_data

"""
动态生成Prefect并调用
"""
def PrefectRun(yaml_path, input_data):
    # 根据流程ID 获取流程和任务参数
    yaml_data = PrefectDealService().parse_flow_yaml(yaml_path=yaml_path)
    # 解析yaml流程文件，并将所有的过程放进去
    prefect = PrefectService(
        yaml_data["flow_name"],
        **input_data
    )

    all_function = yaml_data["all_function"]
    for function in all_function:
        task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
        prefect.append_task(task)

    back = prefect.run()

    return back