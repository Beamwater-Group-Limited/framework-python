# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : spell_controller.py
# @Author        : henryren
# @Time          : 2025/1/16 17:49
# @Function      : 
# @Desc          :
import json

import falcon

from app.error.PyLogger import pyLogger
from app.model.data_item import DataItem, DaContent
from app.model.file.cbt_bpmn import CbtFlowBpmn

logger = pyLogger()
class TaskPreParamsController:
    async def on_get(self, req, resp):
        try:
            # 获取 URL 请求参数：user_id 和 flow_id
            user_id = req.get_param('user_id')  # 获取 user_id 参数
            flow_id = req.get_param('flow_id')  # 获取 flow_id 参数
            element_id = req.get_param('element_id')  # 获取 flow_id 参数
            # 检查参数是否存在
            if not user_id or not flow_id or not element_id:
                resp.status = falcon.HTTP_400
                resp.text = {"status": "error", "message": "缺少参数"}
                return
            cfb = CbtFlowBpmn(author=user_id, file_name=flow_id)
            contents = cfb.find_incoming(element_id=element_id)
            contents = DaContent.obj2dct(contents)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.text = json.dumps(contents)  # 返回 JSON 格式的数据
        except Exception as e:
            # 如果文件读取失败，返回 500 错误
            logger.error(f"BPMN文件读取时发生错误:{str(e)}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": "保存失败"}

