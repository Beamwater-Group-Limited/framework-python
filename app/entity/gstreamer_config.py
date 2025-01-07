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
        self.camera_name = ""  # 监控名称
        self.rtsp_url = ""  # rtsp流地址
        self.encode = ""  # 编码格式
        self.ts_url = "" # 转发地址
        self.process_mount = ""
        self.is_work = ""  #
        self.gstreamer_instance = ""

    def to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'camera_name': self.camera_name,
            'rtsp_url': self.rtsp_url,
            'encode': self.encode,
            'ts_url': self.ts_url,
            'process_mount': self.process_mount,
            'is_work': self.is_work,
            'gstreamer_instance': self.gstreamer_instance
        }

    def all_to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'id': self.id,
            'camera_name': self.camera_name,
            'rtsp_url': self.rtsp_url,
            'encode': self.encode,
            'ts_url': self.ts_url,
            'process_mount': self.process_mount,
            'is_work': self.is_work,
            'gstreamer_instance': self.gstreamer_instance
        }
