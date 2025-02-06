# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : diagram_controller.py
# @Author        : henryren
# @Time          : 2025/1/16 17:18
# @Function      : 
# @Desc          :
from pathlib import Path

import falcon

from app import config
from app.error.PyLogger import pyLogger
from app.model.file.cbt_bpmn import CbtFlowBpmn
from app.model.flow.cbt_bpmn_dao import CbtBpmnDao

logger = pyLogger()

class DiagramController:
    async def on_get(self, req, resp):
        try:
            # 获取 URL 请求参数：user_id 和 flow_id
            user_id = req.get_param('user_id')  # 获取 user_id 参数
            flow_id = req.get_param('flow_id')  # 获取 flow_id 参数
            # 检查参数是否存在
            if not user_id :
                resp.status = falcon.HTTP_400
                resp.text = {"status": "error", "message": "缺少 user_id"}
                return
            if not flow_id:
                # 加载流程
                cfb = CbtFlowBpmn(author=user_id, file_name='Process_1')
            else:
                cfb = CbtFlowBpmn(author=user_id, file_name=flow_id)
            # 设置响应内容类型为 XML
            resp.content_type = "application/xml"
            resp.text = cfb.read_bpmn()  # Falcon 3.x 及以后使用 resp.text 替代 resp.body
            resp.status = falcon.HTTP_200
        except Exception as e:
            # 如果文件读取失败，返回 500 错误
            logger.error(f"读取 BPMN 文件时发生错误:{str(e)}")
            resp.status = falcon.HTTP_500
            resp.text = "无法读取 BPMN 文件"

    async def on_post(self, req, resp):
        # 解析请求体中的 JSON 数据
        try:
            body = await req.media  # Falcon 自动解析为字典
            bpmn_data = body.get("bpmn_data")
            user_id = body.get("user_id")
        except Exception as e:
            logger.error(f"解析请求数据时出错:{str(e)}")
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "无效的请求数据"}
            return

        # 检查 bpmnData 是否存在
        if not bpmn_data:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "无效的请求数据"}
            return
        try:
            # 加载bpmn图
            logger.debug(f'bpmn_数据: \n{bpmn_data}')
            bpmn_tree = CbtFlowBpmn.load_from_unicode_str(bpmn_str=bpmn_data)
            process_id = CbtFlowBpmn.get_process_id_first(bpmn_tree)
            cbt_fb = CbtFlowBpmn(relative_path=f'{user_id}/{process_id}.bpmn')
            cbt_fb.write_bpmn(xml_content=bpmn_data)
            logger.info(f"BPMN 数据已保存到 {cbt_fb.file_path} 文件")
            resp.media = {"status": "success", "message": "保存完成！"}
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error(f"保存 BPMN 数据时出错:{str(e)}",)
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": "保存失败"}
