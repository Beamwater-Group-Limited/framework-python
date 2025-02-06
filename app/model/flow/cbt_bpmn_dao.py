# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_bpmn_dao.py
# @Author        : henryren
# @Time          : 2025/1/19 15:42
# @Function      : 
# @Desc          : 这是个虚，从bpmn文件中抽取值的类
import uuid
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class CbtBpmnDao:
    """
    BPMN 文件的数据访问对象，用于存储和管理 BPMN 文件的主要属性和内容
    """
    bpmn_description: str = field(default="这是由束水系统自动生成的 BPMN 文件")
    bpmn_author: str = field(default="cbtai")  # BPMN 文件作者
    bpmn_name: str = None
    bpmn_path: str = None

    def __post_init__(self):
        """
        初始化后处理：生成 BPMN 文件的 ID 和保存路径
        """
        self.bpmn_path =  f"{self.bpmn_author}/{self.bpmn_name}.bpmn"

    def obj2dct(self) -> Dict:
        """
        将对象转换为字典表示，用于文件存储或序列化
        :return: BPMN 数据的字典表示
        """
        data = self.__dict__
        return data

    @staticmethod
    def as_CbtBpmnDao(dct: Dict):
        """
        从字典数据生成 BpmnDao 对象
        :param dct: 字典表示的 BPMN 数据
        :return: BpmnDao 对象
        """
        bpmn_dao = CbtBpmnDao(
            bpmn_description=dct.get("bpmn_description", "这是由束水系统自动生成的 BPMN 文件"),
            bpmn_author=dct.get("bpmn_author", "cbtai"),
            bpmn_name=dct.get("bpmn_name", str(uuid.uuid4()).replace("-", "")[:8]),
        )
        return bpmn_dao
