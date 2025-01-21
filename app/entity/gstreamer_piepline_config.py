# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : tg
# @File          : Indicia_entity.py
# @Author        : wen
# @Time          : 2022/11/24 13:08
# @Function      : 标注信息
# @Desc          :

class GstreamerPiePlineConfig:

    def __init__(self):
        self.id = ""  # 唯一id
        self.gs_name = ""  # 管道名称
        self.input_data = []  # 管道输入数据
        self.output_type = "" # 管道输出类型
        self.output_data = "" # 管道输出数据
        self.gs_comes = []
        self.gs_gos = []

    def to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'gs_name': self.gs_name,
            'input_data': self.input_data,
            'output_type': self.output_type,
            'output_data': self.output_data,
            'gs_comes': self.gs_comes,
            'gs_gos': self.gs_gos,
        }

    def all_to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'id': self.id,
            'gs_name': self.gs_name,
            'input_data': self.input_data,
            'output_type': self.output_type,
            'output_data': self.output_data,
            'gs_comes': self.gs_comes,
            'gs_gos': self.gs_gos,
        }
