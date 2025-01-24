import base64
import logging
import os
import shutil
import uuid

import falcon
import simplejson as json
import yaml

from app import config
from app.entity.gstreamer_config import GstreamerConfig
from app.entity.gstreamer_piepline_config import GstreamerPiePlineConfig
from app.entity.input_camera import InputCamera
from app.entity.respon_entity import ResponEntity
from app.model.data_item import DataItem, DaType, DaFormat
from app.service.config_service import ConfigService
from app.service.gstreamer_send_voice import play_once
from app.service.gstreamer_service import GstreamerManager

logger = logging.getLogger(config.app_name)

# 设置全局的gstreamer管理功能
gstreamerManager = GstreamerManager()

from gi.repository import Gst

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
                        gstreamer_config.gs_config_name = gstreamer_info["gs_config_name"]
                        gstreamer_config.gs_input_data = gstreamer_info["gs_input_data"]
                        gstreamer_config.gs_output_type = gstreamer_info["gs_output_type"]
                        gstreamer_config.gs_output_data = gstreamer_info["gs_output_data"]
                        gstreamer_config.process_mount = gstreamer_info["process_mount"]
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
            gs_config_id = media["gs_config_id"]
            process_mount = media["process_mount"]

            # 获取管道数据
            dir_path = f"/home/ya/mapdata/gstreamer-config/{gs_config_id}"
            yaml_path = os.path.join(dir_path, "config.yaml")
            with open(yaml_path, 'r') as file:
                existing_data = yaml.safe_load(file) or {}

            gstreamerConfig = GstreamerConfig()
            gstreamerConfig.id = str(uuid.uuid4())
            gstreamerConfig.gs_config_name = existing_data["gs_name"]
            gstreamerConfig.gs_input_data = existing_data["input_data"]
            gstreamerConfig.gs_output_type = existing_data["output_type"]
            gstreamerConfig.gs_output_data = existing_data["output_data"]
            gstreamerConfig.process_mount = process_mount

            camera_data = { }

            for inputValue in gstreamerConfig.gs_input_data:
                if inputValue["type"] == "Stream":
                    yaml_path = f"/home/ya/mapdata/video/{inputValue['data']}.yaml"
                    camera = InputCamera()
                    with open(yaml_path, 'r') as file:
                        existing_data = yaml.safe_load(file) or {}
                        # 遍历字典
                        camera.id = existing_data["id"]
                        camera.rtsp_url = existing_data["rtsp_url"]
                        camera.camera_name = existing_data["camera_name"]
                        camera.encode = existing_data["encode"]
                        camera.is_work = existing_data["is_work"]
                        camera_data = camera.all_to_dict()

            gstreamerManager.start_new_gstreamer(gstreamerConfig.all_to_dict(), camera_data)

            ConfigService().add_input_camera_data(gstreamer_run_yaml_path, gstreamerConfig.id,
                                                  gstreamerConfig.to_dict())

            resp.body = json.dumps(ResponEntity().ok(
                "添加视频流运行成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
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


# 修改运行的流挂载的流程
class UpdateGstreamerProcessMountController(GstreamerController):
    async def on_post(self, req, resp):
        try:
            gstreamer_run_yaml_path = "/home/ya/mapdata/gstreamer_run.yaml"
            media = await req.get_media()
            gstreamer_id = media["gstreamer_id"]
            process_mount = media["process_mount"]
            # 根据id获取流的信息
            with open(gstreamer_run_yaml_path, 'r') as file:
                existing_data = yaml.safe_load(file)
                # 遍历字典
                gstreamer_info = existing_data[gstreamer_id]
            gstreamer_config = GstreamerConfig()
            gstreamer_config.id = gstreamer_id
            gstreamer_config.ts_url = gstreamer_info["ts_url"]
            gstreamer_config.process_mount = process_mount
            gstreamer_config.rtsp_url = gstreamer_info["rtsp_url"]
            gstreamer_config.camera_name = gstreamer_info["camera_name"]
            gstreamer_config.encode = gstreamer_info["encode"]
            gstreamer_config.is_work = gstreamer_info["is_work"]

            # 将运行流的信息信息添加到yaml文件中
            ConfigService().update_input_camera_data(gstreamer_run_yaml_path, gstreamer_config.id,
                                                     gstreamer_config.to_dict())

            resp.body = json.dumps(ResponEntity().ok(
                "修改运行的流挂载的流程成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("修改运行的流挂载的流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("修改运行的流挂载的流程失败", e))
            resp.status = falcon.HTTP_500


# 通过gstreamer播放声音
class SendVoiceController(GstreamerController):
    async def on_post(self, req, resp):
        try:
            media = await req.get_media()
            text = media["text"]
            play_once(text)
            resp.body = json.dumps(ResponEntity().ok(
                "通过gstreamer播放声音成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("通过gstreamer播放声音失败", e)
            resp.body = json.dumps(ResponEntity().exception("通过gstreamer播放声音失败", e))
            resp.status = falcon.HTTP_500


# 新增gstreamer管道配置
class AddGstreamerConfigController(GstreamerController):
    async def on_post(self, req, resp):
        try:
            media = await req.get_media()
            gsName = media["gstreamer_name"]
            gsInputData = media["gstreamer_input_data"]
            gsOutputType = media["gstreamer_output_type"]
            gsOutputData = media["gstreamer_output_data"]

            folder_id = str(uuid.uuid4())
            # Ensure the directory exists
            config_dir = f"/home/ya/mapdata/gstreamer_yaml/cbtai"
            os.makedirs(config_dir, exist_ok=True)

            # 判断gstreamer_input_type的类型，如果是img或video，需要将文件保存
            # if gsInputType == "Image":
            #     image_data = base64.b64decode(gsInputData)
            #     image_path = f"{config_dir}/image.png"
            #     with open(image_path, "wb") as image_file:
            #         image_file.write(image_data)
            #     gsInputData = image_path
            # elif gsInputType == "Video":
            #     video_data = base64.b64decode(gsInputData)
            #     video_path = f"{config_dir}/video.mp4"
            #     with open(video_path, 'wb') as video_file:
            #         video_file.write(video_data)
            #     gsInputData = video_path
            # elif gsInputType == "Stream":
            #     print("stream input type")
            # 添加配置文件
            gstreamerPieplineConfig = GstreamerPiePlineConfig()
            gstreamerPieplineConfig.id = folder_id
            gstreamerPieplineConfig.gs_name = gsName
            gstreamerPieplineConfig.input_data = gsInputData
            gstreamerPieplineConfig.output_type = gsOutputType
            gstreamerPieplineConfig.output_data = gsOutputData
            default_comes = [
                DataItem(DaType.AUDIO, DaFormat.fbase64, "接收到的声音").obj2dct()
            ]
            default_gos = [
                DataItem(DaType.AUDIO, DaFormat.fbase64, "翻译后的声音").obj2dct()
            ]

            gstreamerPieplineConfig.gs_comes = default_comes

            gstreamerPieplineConfig.gs_gos = default_gos

            yaml_path = f"{config_dir}/{folder_id}.yaml"

            # 将摄像头信息添加到yaml文件中
            with open(yaml_path, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump(gstreamerPieplineConfig.all_to_dict(), file)

            resp.body = json.dumps(ResponEntity().ok(
                "新增gstreamer管道配置成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("新增gstreamer管道配置失败", e)
            resp.body = json.dumps(ResponEntity().exception("新增gstreamer管道配置失败", e))
            resp.status = falcon.HTTP_500


# 获取管道配置数据
class GetGstreamerPiePlineConfigController(GstreamerController):
    async def on_get(self, req, resp):
        try:
            gstreamer_dir = "/home/ya/mapdata/gstreamer_yaml/cbtai"
            back = []
            if os.path.exists(gstreamer_dir):
                for f in os.listdir(gstreamer_dir):
                    if f.endswith(".yaml"):
                        yaml_path = os.path.join(gstreamer_dir, f)
                        with open(yaml_path, 'r') as file:
                            existing_data = yaml.safe_load(file) or {}
                            # 遍历字典
                            gs_piepline_config = GstreamerPiePlineConfig()
                            gs_piepline_config.id = existing_data["id"]
                            gs_piepline_config.gs_name = existing_data["gs_name"]
                            if existing_data["output_type"] == "Audio":
                                gs_piepline_config.output_type = "声音播放"
                            else:
                                gs_piepline_config.output_type = "视频流输出"

                            gs_piepline_config.input_data = existing_data["input_data"]
                            gs_piepline_config.output_data = existing_data["output_data"]
                            gs_piepline_config.gs_comes = existing_data["gs_comes"]
                            gs_piepline_config.gs_gos = existing_data["gs_gos"]

                            back.append(gs_piepline_config.all_to_dict())

            resp.body = json.dumps(ResponEntity().ok(
                "获取摄像头数据成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取摄像头数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取摄像头数据失败", e))
            resp.status = falcon.HTTP_500


# 删除管道配置数据
class DelGstreamerPiePlineConfigController(GstreamerController):
    async def on_get(self, req, resp):
        try:
            gstreamer_config_id = req.params["id"]
            gstreamer_path = f"/home/ya/mapdata/gstreamer_yaml/cbtai/${gstreamer_config_id}.yaml"
            if os.path.exists(gstreamer_path):
                os.remove(gstreamer_path)

            resp.body = json.dumps(ResponEntity().ok(
                "删除管道配置数据成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("删除管道配置数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("删除管道配置数据失败", e))
            resp.status = falcon.HTTP_500


# 根据ID获取管道数据
class GetSingleGstreamerPiePlineConfigController(GstreamerController):
    async def on_get(self, req, resp):
        try:
            gs_config_id = req.params["id"]
            yaml_path = f"/home/ya/mapdata/gstreamer_yaml/cbtai/${gs_config_id}.yaml"
            with open(yaml_path, 'r') as file:
                existing_data = yaml.safe_load(file) or {}
                # 遍历字典
                gs_piepline_config = GstreamerPiePlineConfig()
                gs_piepline_config.id = existing_data["id"]
                gs_piepline_config.gs_name = existing_data["gs_name"]
                if existing_data["output_type"] == "Audio":
                    gs_piepline_config.output_type = "声音播放"
                else:
                    gs_piepline_config.output_type = "视频流输出"

                gs_piepline_config.input_data = existing_data["input_data"]
                gs_piepline_config.output_data = existing_data["output_data"]
                gs_piepline_config.gs_comes = existing_data["gs_comes"]
                gs_piepline_config.gs_gos = existing_data["gs_gos"]

            resp.body = json.dumps(ResponEntity().ok(
                "根据ID获取管道数据成功",
                gs_piepline_config.all_to_dict()
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("根据ID获取管道数据失败", e)
            resp.body = json.dumps(ResponEntity().exception("根据ID获取管道数据失败", e))
            resp.status = falcon.HTTP_500
