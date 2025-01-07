# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : tg
# @File          : Indicia_entity.py
# @Author        : wen
# @Time          : 2022/11/24 13:08
# @Function      : 标注信息
# @Desc          :

class InputCamera:

    def __init__(self):
        self.id = ""  # 唯一id
        self.camera_name = ""  # 监控名称
        self.rtsp_url = ""  # rtsp流地址
        self.encode = ""  # 编码格式
        self.is_work = ""  # 编码格式

    def to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'camera_name': self.camera_name,
            'rtsp_url': self.rtsp_url,
            'encode': self.encode,
            'is_work': self.is_work
        }

    def all_to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'id': self.id,
            'camera_name': self.camera_name,
            'rtsp_url': self.rtsp_url,
            'encode': self.encode,
            'is_work': self.is_work
        }
