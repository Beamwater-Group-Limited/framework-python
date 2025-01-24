# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_model_info.py
# @Author        : henryren
# @Time          : 2025/1/9 19:07
# @Function      : 
# @Desc          :
from dataclasses import dataclass
from typing import Dict

from app import config
from app.error.PyTFError import catchexcept
from app.model.cbt_interface_dao import CbtInterfaceDao, CbtInterfaceBpmn
from app.model.file.cbt_yaml import CbtModelYaml

@dataclass
class CbtModelBpmn:
    id:str
    model_name:str
    interface_bpmn:[CbtInterfaceBpmn] = None
    def obj2dct(self):
        some = self.__dict__
        if self.interface_bpmn is not None:
            some['interface_bpmn'] = [entry.obj2dct() for entry in self.interface_bpmn]
        return some
    @staticmethod
    def as_CbtModelBpmn(dct: Dict):
        some = CbtModelBpmn(dct.get('id'), dct.get('model_name'))
        interface_bpmn = dct.get('interface_bpmn', None)
        some.interface_bpmn = [CbtInterfaceBpmn.as_CbtInterfaceBpmn(di) for di in interface_bpmn] if interface_bpmn is not None else None
        return some

# 存储模型的信息
@dataclass
class CbtModelInfoDao:
    company_name:str
    model_name:str
    revision:str
    model_interfaces:[CbtInterfaceDao] = None
    model_class:str = None
    model_id:str = None
    model_path:str = None
    model_config_path:str = None
    def __post_init__(self):
        self.model_id = f"{self.company_name}/{self.model_name}/{self.revision}"
        # todo 需要修改为相对路径
        self.model_path = str(config.basepath / 'hub' / f"models--{self.company_name}--{self.model_name}")
        self.model_config_path = CbtModelYaml(f'{self.company_name}/{self.model_name}--{self.revision}.yaml').yaml_relative_path

    def obj2dct(self):
        some = self.__dict__
        if self.model_interfaces is not None:
            some["model_interfaces"] = [entry.obj2dct() for entry in self.model_interfaces]
        return some

    @staticmethod
    def as_CbtModelInfo(dct: Dict):
        """
        从字典重新构建对象
        :param dct: 字典输入
        :return: 重建的 CbtModelInfoDao 对象
        """
        cbtModelInfoDat =  CbtModelInfoDao(dct.get("company_name"), dct.get("model_name"), dct.get("revision"))
        if dct.get("model_interfaces"):
            mis = [CbtInterfaceDao.as_CbtInterfaceDao(dc) for dc in dct.get("model_interfaces")]
            cbtModelInfoDat.model_interfaces = mis
        return cbtModelInfoDat

    @catchexcept(f'CbtModelInfoDao:to_bpmn:')
    def to_bpmn(self)->'CbtModelBpmn':
        some = CbtModelBpmn(self.model_id, self.model_name)
        some.interface_bpmn = [interface.to_bpmn() for interface in self.model_interfaces] if self.model_interfaces else None
        return some

    def showContent(self):
        print(f"CbtModelInfoDao展示内容")
        for key, value in self.__dict__.items():
            if key == "model_interfaces":
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
