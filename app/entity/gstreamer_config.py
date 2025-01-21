# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : tg
# @File          : Indicia_entity.py
# @Author        : wen
# @Time          : 2022/11/24 13:08
# @Function      : 标注信息
# @Desc          :

class GstreamerConfig:

    def __init__(self):
        self.id = ""  # 唯一id
        self.gs_config_name = ""  # 管道名称
        self.gs_input_data = []  # 管道输入数据
        self.gs_output_type = "" # 管道输出类型
        self.gs_output_data = ""  # 管道输出数据
        self.process_mount = "" # 流程挂载
        self.gstreamer_instance = ""

    def to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'gs_config_name': self.gs_config_name,
            'gs_input_data': self.gs_input_data,
            'gs_output_type': self.gs_output_type,
            'gs_output_data': self.gs_output_data,
            'process_mount': self.process_mount,
            'gstreamer_instance': self.gstreamer_instance
        }

    def all_to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'id': self.id,
            'gs_config_name': self.gs_config_name,
            'gs_input_data': self.gs_input_data,
            'gs_output_type': self.gs_output_type,
            'gs_output_data': self.gs_output_data,
            'process_mount': self.process_mount,
            'gstreamer_instance': self.gstreamer_instance
        }
