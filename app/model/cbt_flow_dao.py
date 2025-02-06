# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_model_info.py
# @Author        : henryren
# @Time          : 2025/1/9 19:07
# @Function      : 
# @Desc          :
import uuid
from dataclasses import dataclass, field
from typing import Dict

from app import config
from app.model.cbt_interface_dao import CbtInterfaceDao
from app.model.file.cbt_yaml import CbtFlowYaml


# 存储流的信息
@dataclass
class CbtFlowDao:
    flow_describe:str = field(default='这是一个束水任务流')
    flow_author: str = field(default=config.ORGANIZATION)
    flow_name:str = field(default_factory= lambda: str(uuid.uuid4()).replace('-', '')[:8])  # 自动生成 UUID
    flow_id:str = None
    flow_interfaces:[CbtInterfaceDao] = None
    flow_json:str = None
    flow_yaml_path:str = None
    def __post_init__(self):
        self.flow_id = f"{self.flow_author}/{self.flow_name}"
        self.flow_yaml_path = CbtFlowYaml(f'{self.flow_author}/{self.flow_name}.yaml').yaml_relative_path

    def obj2dct(self):
        some = self.__dict__
        if self.flow_interfaces is not None:
            some["flow_interfaces"] = [entry.obj2dct() for entry in self.flow_interfaces]
        return some

    @staticmethod
    def as_CbtFlowDao(dct: Dict):
        """
        从字典重新构建对象
        :param dct: 字典输入
        :return: 重建的 CbtModelInfoDao 对象
        """
        cbtFlowDao =  CbtFlowDao(dct.get("flow_describe"), dct.get("flow_author"), dct.get("flow_name"))
        if dct.get("flow_interfaces"):
            fis = [CbtInterfaceDao.as_CbtInterfaceDao(dc) for dc in dct.get("flow_interfaces")]
            cbtFlowDao.flow_interfaces = fis
        return cbtFlowDao

    def showContent(self):
        print(f"CbtFlowDao展示内容")
        for key, value in self.__dict__.items():
            if key == "flow_interfaces":
                if value is None:
                    print(f"{key}: None")
                else:
                    for data in value:
                        data.showContent()
            else:
                if value is None:
                    print(f"{key}: None")
                else:
                    print(f"{key}: {value}")
