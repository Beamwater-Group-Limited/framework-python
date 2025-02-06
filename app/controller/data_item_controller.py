# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : data_format_controller.py
# @Author        : henryren
# @Time          : 2025/1/16 17:49
# @Function      : DataFormatController - 提供DataFormat可选项
# @Desc          :
import json

import falcon

from app.model.data_item import DaType, DaFormat


class DataFormatController:
    def __init__(self):
        self.data_formats = DaFormat.obj2dct()

    async def on_get(self, req, resp):
        """
        处理 GET 请求，返回支持的 DataFormat 可选项列表
        """
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(self.data_formats)  # 返回 JSON 格式的数据


class DataTypeController:
    def __init__(self):
        self.data_types = DaType.obj2dct()

    async def on_get(self, req, resp):
        """
        处理 GET 请求，返回支持的 DataFormat 可选项列表
        """
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(self.data_types)  # 返回 JSON 格式的数据
