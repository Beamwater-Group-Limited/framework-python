# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : prefect_seria
# @File          : prefect_service.py
# @Author        : Yuan
# @Time          : 2024/10/11 16:35
# @Function      : 
# @Desc          :
import json

import requests
import yaml
# 动态生成多个任务
from prefect import flow

from app.entity.task_node import TaskNode
from app.error.PyLogger import pyLoggerFirst
from app.model.come_entity import ComeEntity
from app.model.context_entity import ContextEntity
from app.model.data_item import DataItem, DaFormat, DaType
from app.prompts import llava_prompts

logger = pyLoggerFirst()

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
    # yaml_data = PrefectDealService().parse_flow_yaml(yaml_path=yaml_path)
    # # 解析yaml流程文件，并将所有的过程放进去
    # prefect = PrefectService(
    #     yaml_data["flow_name"],
    #     **input_data
    # )
    #
    # all_function = yaml_data["all_function"]
    # for function in all_function:
    #     task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
    #     prefect.append_task(task)
    #
    # back = prefect.run()

    system_prompt = llava_prompts.system_prompt_new
    cheng_schema = llava_prompts.cheng_schema
    # todo 增加本地数据测试
    image_left = "https://www.baidu.com/img/bd_logo1.png"
    image_right = "http://images.cocodataset.org/val2017/000000039769.jpg"
    # image_quest = "https://q6.itc.cn/q_70/images03/20240229/d3f2bf2b8bb24f65bebf0e9e1b7e8910.jpeg"
    # 创建数据
    comes = [
        DataItem(content="process"),
        DataItem(DaType.APPLICATION, DaFormat.fstring, content=json.dumps(cheng_schema)),
        DataItem(content='关于图片的问题的回答字数不要超过 10个字'),
        # DataItem(DaType.IMAGE, DaFormat.furl, content=f"{image_left}"),
        DataItem(DaType.IMAGE, DaFormat.fbase64, content=f"{input_data}"),
        # DataItem(DaType.IMAGE, DaFormat.furl, content=f"{image_right}"),
        DataItem(content="描述一下图片内容\n")
    ]
    comeEntity = ComeEntity().setup(comes=comes, context=ContextEntity())
    # 定义请求的 URL
    url = "http://192.168.0.70:28286/v1/process"  # 替换为目标 URL

    # 定义 JSON 数据
    payload = comeEntity.obj2dct()
    # 发送 POST 请求
    headers = {"Content-Type": "application/json"}
    logger.debug(f'url:\n{url}')
    logger.debug(f'payload:\n{payload}')
    logger.debug(f'headers\n{headers}')
    response = requests.post(url, json=payload, headers=headers)
    hao_comeEntity = ComeEntity.as_ComeEntity(response.json())
    logger.debug(f'响应:{hao_comeEntity.obj2dct()}')

    return ""