# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : model_bpmn_controller.py
# @Author        : henryren
# @Time          : 2025/1/17 00:21
# @Function      : 
# @Desc          :
import json
import traceback

import falcon

from app.model.pipeline.cbt_pipeline_file_manager import CbtPipelineFileManager
from app.model.respon_entity import ResponEntity

class PipelineController:
    # 异步函数，用于处理 HTTP GET 请求
    async def on_get(self, req, resp):
        try:
            # 获取 URL 请求参数：user_id
            user_id = req.get_param('user_id')  # 获取 user_id 参数
            # 检查参数是否存在
            if not user_id :
                resp.status = falcon.HTTP_400
                resp.text = {"status": "error", "message": "缺少 user_id 参数"}
                return
            # 调用 CbtPipelineFileManager 的 scanPipelineDir 方法获取所有GStreamer管道数据
            pipeline = CbtPipelineFileManager(user_id).scanPipelineDir()
            # 设置响应内容类型为 JSON 格式
            resp.content_type = 'application/json'
            # 将模型信息转换为 JSON 字符串并设置为响应文本
            resp.text = json.dumps(pipeline)
            # 设置响应状态码为 HTTP 200（成功）
            resp.respon_status = falcon.HTTP_200
        except Exception as e:
            traceback.print_exc()
            # 捕获异常后设置响应状态码为 HTTP 500（内部服务器错误）
            resp.respon_status = falcon.HTTP_500
            # 使用 ResponEntity 返回异常信息并转换为 JSON 字符串
            resp.text = json.dumps(ResponEntity().exception(str(e)))