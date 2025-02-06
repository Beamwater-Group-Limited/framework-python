# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_model_interface.py
# @Author        : henryren
# @Time          : 2025/1/12 17:04
# @Function      : 
# @Desc          : 模型的接口类型
from dataclasses import dataclass
from typing import Dict

from app.error.PyTFError import catchexcept
from app.model.data_item import DataItem

@dataclass
class CbtPipelineInputDao:
    data:str
    type: str

    def obj2dct(self) ->Dict:
        some = self.__dict__
        return some

    @staticmethod
    def as_CbtPipelineInputDao(dct: Dict):
        some = CbtPipelineInputDao(
            data=dct.get('data'),
            type=dct.get('type')
        )
        return some