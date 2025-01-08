# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : prefect_seria
# @File          : prefect_service.py
# @Author        : Yuan
# @Time          : 2024/10/11 16:35
# @Function      : 
# @Desc          :
from gi.repository import Gst, GObject, GLib
Gst.init(None)

from app.service.gstreamer_pieline_service import GstreamerPiePline

import multiprocessing

multiprocessing.set_start_method('fork')

class GstreamerManager:
    """
    gstreamer流程管理类
    """

    def __init__(self):
        self.gstreamer_piepline = []

    # 开启一个gstreamer
    def start_new_gstreamer(self, gstreamer_config):
        gstreamer = GstreamerPiePline(gstreamer_config)
        process = multiprocessing.Process(target=gstreamer.start)
        process.daemon = True  # 设置为守护进程
        process.start()
        gstreamer_config['gstreamer_instance'] = gstreamer
        self.gstreamer_piepline.append(gstreamer_config)
        return gstreamer_config

    # 暂停一个gstreamer
    def stop_gstreamer(self, gstreamer_config_id):
        for config in self.gstreamer_piepline:
            if config.get('id') == gstreamer_config_id:
                if config.get('gstreamer_instance') is not None:
                    config['gstreamer_instance'].stop()
                self.gstreamer_piepline.remove(config)
        return "success"

    # 获取所有的gstreamer
    def get_all_gstreamer(self):
        return self.gstreamer_piepline