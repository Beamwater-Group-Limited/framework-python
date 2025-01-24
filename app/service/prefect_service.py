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
from app.error.PyLogger import pyLoggerFirst

logger = pyLoggerFirst()


class PrefectService:
    def __init__(self, flow_name: str, param_data) -> None:
        self.task_list = []
        self.flow_name = flow_name
        self.param_data = param_data

    # 流附加任务
    def append_task(self, task) -> None:
        self.task_list.append(task)

    # 执行流
    @flow(log_prints=True)
    def run(self) -> str:
        # 循环调用task执行
        for task in self.task_list:
            print(f"当前处理的任务为{task.task_name}")
            self.param_data = task.run(self.param_data)
        return self.param_data


class PrefectDealService:
    def parse_flow_yaml(self, yaml_path):
        with open(yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)
        return existing_data


"""
动态生成Prefect并调用
"""


def PrefectRun(bpmn_data, param_data):
    # 解析yaml流程文件，并将所有的过程放进去
    prefect = PrefectService(
        bpmn_data["process"],
        param_data
    )

    all_function = bpmn_data["user_tasks"]
    for function in all_function:
        # 判断function是否是最后一个任务
        is_last_task = all_function.index(function) == len(all_function) - 1

        task = TaskNode(function["model_id"], function["api_endpoint"], function["up_params_parsed"],
                        function["down_params_parsed"], is_last_task)

        prefect.append_task(task)

    back = prefect.run()

    return back
