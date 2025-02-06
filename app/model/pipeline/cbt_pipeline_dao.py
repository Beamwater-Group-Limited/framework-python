# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_pipeline_dao.py
# @Author        : henryren
# @Time          : 2025/1/19 15:42
# @Function      : 
# @Desc          : 这是个虚，从yaml文件中抽取值的类
import uuid
from dataclasses import dataclass, field
from typing import Dict, List

from app.model.data_item import DataItem, DaType, DaFormat
from app.model.file.cbt_yaml import CbtPipelineYaml
from app.model.pipeline.cbt_pipeline_input_dao import CbtPipelineInputDao


@dataclass
class CbtPipelineDao:
    """
    YAML 文件的数据访问对象，用于存储和管理 YAML 文件的主要属性和内容
    """
    id: str = field(default="这是一个UUID")
    author: str = field(default="cbtai")  # BPMN 文件作者
    describe: str = None
    name: str = None
    yaml_input_data: [CbtPipelineInputDao] = None
    yaml_output_type: str = None
    yaml_output_data: str = None
    yaml_comes: [] = None
    yaml_gos: [] = None

    yaml_path: str = None

    def __post_init__(self):
        """
        初始化后处理：生成 BPMN 文件的 ID 和保存路径
        """
        self.yaml_path = CbtPipelineYaml(f"{self.author}/{self.name}.yaml").yaml_relative_path

    def obj2dct(self) -> Dict:
        """
        将对象转换为字典表示，用于文件存储或序列化
        :return: YAML 数据的字典表示
        """
        data = self.__dict__
        data["id"] = f"{data['author']}/{data['name']}"
        return data

    @staticmethod
    def as_CbtPipelineDao(dct: Dict):
        """
        从字典数据生成 BpmnDao 对象
        :param dct: 字典表示的 BPMN 数据
        :return: BpmnDao 对象
        """
        bpmn_dao = CbtPipelineDao(
            author=dct.get("yaml_author", "cbtai"),
            name=dct.get("id", None),
            describe=dct.get("gs_name", None),
            yaml_input_data=dct.get("input_data", None),
            yaml_output_type=dct.get("output_type", None),
            yaml_output_data=dct.get("output_data", None),
            yaml_comes=dct.get("gs_comes", None),
            yaml_gos=dct.get("gs_gos", None)
        )
        return bpmn_dao