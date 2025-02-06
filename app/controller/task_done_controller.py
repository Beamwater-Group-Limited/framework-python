# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : task_done_controller.py
# @Author        : henryren
# @Time          : 2024/12/23 00:40
# @Function      : 
# @Desc          :
import json

import falcon

from app.error.PyLogger import pyLogger
from app.model.respon_entity import ResponEntity
from app.service.TaskStatePushService import TaskStatePushService

logger = pyLogger()


class TaskDoneController:
    async def on_post(self, req, resp):
        """
        启动长时间运行任务
        """
        logger.info("收到 POST 请求：访问 /task_done 接口")
        # 异步解析请求体数据
        try:
            media = await req.get_media()
        except Exception as e:
            logger.error(f"解析请求数据时出错: {str(e)}")
            resp.respon_status = falcon.HTTP_400
            resp.text = json.dumps(ResponEntity().exception("无效的请求数据"))
            return

        task_id = media.get('task_id', None)
        if task_id:
            logger.info(f"task_id: {task_id}")
        else:
            logger.error("缺少必需的 task_id 参数")
        # 推送 WebSocket 状态更新
        await TaskStatePushService.websocket_manager.broadcast(str(media))
        # 返回任务状态
        resp.text = json.dumps(ResponEntity().ok("测试成功", media))
        resp.respon_status = falcon.HTTP_200
