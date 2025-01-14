import logging
import os
import uuid

import falcon
import simplejson as json
import yaml

from app import config
from app.entity.input_camera import InputCamera
from app.entity.respon_entity import ResponEntity

logger = logging.getLogger(config.app_name)


class VideoController:
    def __init__(self):
        pass

# 获取摄像头的yaml数据
class GetInputCameraController(VideoController):
    async def on_get(self, req, resp):
        try:
            yaml_dir = "/home/ya/mapdata/video"
            back = []
            if os.path.exists(yaml_dir):
                yaml_files = [os.path.join(yaml_dir, file) for file in os.listdir(yaml_dir) if file.endswith(".yaml")]
                for yaml_file in yaml_files:
                    with open(yaml_file, 'r') as file:
                        existing_data = yaml.safe_load(file) or {}
                        # 遍历字典
                        camera = InputCamera()
                        camera.id = existing_data["id"]
                        camera.rtsp_url = existing_data["rtsp_url"]
                        camera.camera_name = existing_data["camera_name"]
                        camera.encode = existing_data["encode"]
                        camera.is_work = existing_data["is_work"]
                        back.append(camera.all_to_dict())
            resp.body = json.dumps(ResponEntity().ok(
                "获取摄像头数据成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取摄像头数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取摄像头数据失败", e))
            resp.status = falcon.HTTP_500


# 添加摄像头数据
class AddInputCameraController(VideoController):
    async def on_post(self, req, resp):
        try:
            camera = InputCamera()
            media = await req.get_media()
            camera.rtsp_url = media["rtsp_url"]
            camera.encode = media["encode"]
            camera.camera_name = media["camera_name"]
            camera.is_work = media["is_work"]
            camera.id = str(uuid.uuid4())
            # 定义摄像头配置文件的地址
            yaml_dir = "/home/ya/mapdata/video"
            if not os.path.exists(yaml_dir):
                os.makedirs(yaml_dir)
            yaml_path = os.path.join(yaml_dir, f"{camera.id}.yaml")

            # 将摄像头信息添加到yaml文件中
            with open(yaml_path, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump(camera.all_to_dict(), file)
            resp.body = json.dumps(ResponEntity().ok(
                "添加摄像头数据成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("添加摄像头数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("添加摄像头数据失败", e))
            resp.status = falcon.HTTP_500


# 修改摄像头数据
class UpdateInputCameraController(VideoController):
    async def on_post(self, req, resp):
        try:
            camera = InputCamera()
            media = await req.get_media()
            camera.id = media["id"]
            camera.rtsp_url = media["rtsp_url"]
            camera.encode = media["encode"]
            camera.camera_name = media["camera_name"]
            camera.is_work = media["is_work"]
            # 定义摄像头配置文件的地址
            yaml_dir = "/home/ya/mapdata/video"
            yaml_path = os.path.join(yaml_dir, f"{camera.id}.yaml")

            # 将摄像头信息添加到yaml文件中
            with open(yaml_path, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump(camera.all_to_dict(), file)
            resp.body = json.dumps(ResponEntity().ok(
                "修改摄像头数据成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("修改摄像头数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("修改摄像头数据失败", e))
            resp.status = falcon.HTTP_500


# 删除摄像头数据
class DelInputCameraController(VideoController):
    async def on_get(self, req, resp):
        try:
            camera_id = req.params["id"]
            yaml_path = f"/home/ya/mapdata/video/{camera_id}.yaml"
            if os.path.exists(yaml_path):
                os.remove(yaml_path)

            resp.body = json.dumps(ResponEntity().ok(
                "删除摄像头数据成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("删除摄像头数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("删除摄像头数据失败", e))
            resp.status = falcon.HTTP_500

# 获取单个摄像头数据
class GetSingleInputCameraController(VideoController):
    async def on_get(self, req, resp):
        try:
            camera_id = req.params["id"]
            yaml_path = f"/home/ya/mapdata/video/{camera_id}.yaml"
            camera = InputCamera()
            with open(yaml_path, 'r') as file:
                existing_data = yaml.safe_load(file) or {}
                # 遍历字典
                camera.id = existing_data["id"]
                camera.rtsp_url = existing_data["rtsp_url"]
                camera.camera_name = existing_data["camera_name"]
                camera.encode = existing_data["encode"]
                camera.is_work = existing_data["is_work"]

            resp.body = json.dumps(ResponEntity().ok(
                "获取单个摄像头数据成功",
                camera.all_to_dict()
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取单个摄像头数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取单个摄像头数据失败", e))
            resp.status = falcon.HTTP_500