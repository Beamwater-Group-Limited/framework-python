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

from app.model.model.cbt_model_file import CbtModelFile
from app.model.model.cbt_model_info_dao import CbtModelInfoDao
from app.model.respon_entity import ResponEntity

class ModelBpmnController:
    # 异步函数，用于处理 HTTP GET 请求
    async def on_get(self, req, resp):
        try:
            # 调用 CbtModelFile 的 scanModelDir 方法获取所有模型信息
            models = CbtModelFile().scanModelDir()
            # 过滤掉为None的数据
            models = [model for model in models if model is not None]
            # 将每个模型转换为 BPMN 格式后再转换为字典格式
            chengs = [CbtModelInfoDao.as_CbtModelInfo(model).to_bpmn() for model in models]
            cheng = [cheng.obj2dct() for cheng in chengs]
            # 设置响应内容类型为 JSON 格式
            resp.content_type = 'application/json'
            # 将模型信息转换为 JSON 字符串并设置为响应文本
            resp.text = json.dumps(cheng)
            # 设置响应状态码为 HTTP 200（成功）
            resp.respon_status = falcon.HTTP_200
        except Exception as e:
            traceback.print_exc()
            # 捕获异常后设置响应状态码为 HTTP 500（内部服务器错误）
            resp.respon_status = falcon.HTTP_500
            # 使用 ResponEntity 返回异常信息并转换为 JSON 字符串
            resp.text = json.dumps(ResponEntity().exception(str(e)))