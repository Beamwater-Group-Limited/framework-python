import logging
import os
import uuid

import falcon
import simplejson as json
import yaml

from app import config
from app.entity.gstreamer_config import GstreamerConfig
from app.entity.respon_entity import ResponEntity
from app.service.config_service import ConfigService
from app.service.gstreamer_service import GstreamerManager

logger = logging.getLogger(config.app_name)

# 设置全局的gstreamer管理功能
gstreamerManager = GstreamerManager()

from gi.repository import Gst, GObject, GLib
Gst.init(None)

class GstreamerController:
    def __init__(self):
        pass

# 获取gstreamer流运行
class GetAllGstreamerController(GstreamerController):
    async def on_get(self, req, resp):
        try:
            gstreamer_run_yaml_path = "/home/ya/mapdata/gstreamer_run.yaml"
            # 判断文件是否存在
            back = []
            if os.path.exists(gstreamer_run_yaml_path):
                # 如果文件已存在，读取文件中的内容
                with open(gstreamer_run_yaml_path, 'r') as file:
                    existing_data = yaml.safe_load(file)
                    # 遍历字典
                    for gstreamer_id, gstreamer_info in existing_data.items():
                        gstreamer_config = GstreamerConfig()
                        gstreamer_config.id = gstreamer_id
                        gstreamer_config.ts_url = gstreamer_info["ts_url"]
                        gstreamer_config.process_mount = gstreamer_info["process_mount"]
                        gstreamer_config.rtsp_url = gstreamer_info["rtsp_url"]
                        gstreamer_config.camera_name = gstreamer_info["camera_name"]
                        gstreamer_config.encode = gstreamer_info["encode"]
                        gstreamer_config.is_work = gstreamer_info["is_work"]
                        back.append(gstreamer_config.all_to_dict())

            resp.body = json.dumps(ResponEntity().ok(
                "获取gstreamer流运行成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取gstreamer流运行失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取gstreamer流运行失败", e))
            resp.status = falcon.HTTP_500


# 添加gstreamer流运行
class AddGstreamerController(GstreamerController):
    async def on_post(self, req, resp):
        try:
            gstreamer_run_yaml_path = "/home/ya/mapdata/gstreamer_run.yaml"
            media = await req.get_media()
            camera_id = media["camera_id"]
            ts_url = media["ts_url"]
            process_mount = media["process_mount"]

            gstreamerConfig = GstreamerConfig()
            gstreamerConfig.id = str(uuid.uuid4())
            gstreamerConfig.ts_url = ts_url
            gstreamerConfig.process_mount = process_mount

            # 获取摄像头数据
            yaml_dir = "/home/ya/mapdata/video"
            yaml_path = os.path.join(yaml_dir, f"{camera_id}.yaml")
            if os.path.exists(yaml_path):
                with open(yaml_path, 'r') as file:
                    existing_data = yaml.safe_load(file) or {}
                # 遍历字典
                gstreamerConfig.rtsp_url = existing_data["rtsp_url"]
                gstreamerConfig.camera_name = existing_data["camera_name"]
                gstreamerConfig.encode = existing_data["encode"]

                gstreamerManager.start_new_gstreamer(gstreamerConfig.all_to_dict())

                ConfigService().add_input_camera_data(gstreamer_run_yaml_path, gstreamerConfig.id, gstreamerConfig.to_dict())

                resp.body = json.dumps(ResponEntity().ok(
                    "添加视频流运行成功",
                    "success"
                ))
                resp.status = falcon.HTTP_200
            else:
                resp.body = json.dumps(ResponEntity().exception("添加视频流运行失败", Exception("未找到摄像头数据")))
                resp.status = falcon.HTTP_500
        except Exception as e:
            logger.error("添加视频流运行失败", e)
            resp.body = json.dumps(ResponEntity().exception("添加视频流运行失败", e))
            resp.status = falcon.HTTP_500


# 暂停运行的流
class PauseGstreamerController(GstreamerController):
    async def on_get(self, req, resp):
        try:
            gstreamer_id = req.params["id"]
            # 删除id摄像头信息
            gstreamer_run_yaml_path = "/home/ya/mapdata/gstreamer_run.yaml"
            ConfigService().del_input_camera_data(gstreamer_run_yaml_path, gstreamer_id)

            resp.body = json.dumps(ResponEntity().ok(
                "暂停运行的流成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("暂停运行的流失败", e)
            resp.body = json.dumps(ResponEntity().exception("暂停运行的流失败", e))
            resp.status = falcon.HTTP_500