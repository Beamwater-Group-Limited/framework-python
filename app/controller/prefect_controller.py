import ast
import base64
import logging
import os

import cv2
import simplejson as json
import falcon
import yaml

from app import config
from app.entity.gstreamer_piepline_config import GstreamerPiePlineConfig
from app.entity.output_data import OutputData
from app.entity.respon_entity import ResponEntity
from app.entity.task_node import TaskNode
from app.model.data_item import DataItem, DaType, DaFormat
from app.model.model.cbt_model_file import CbtModelFile
from app.model.parsed_bpmn.bpmn_entity import parsed_data_to_entity
from app.model.prefect_run.req_parameter import ReqParameter
from app.pipeline.deal_voice_pipeline import DealVoicePipeline
from app.service.prefect_service import PrefectService, PrefectDealService, PrefectRun
from app.untils.bpmn_parser import parse_bpmn_and_params

logger = logging.getLogger(config.app_name)


class PrefectController:
    def __init__(self):
        pass


# 测试流程
class TestRunFlowController(PrefectController):
    async def on_post(self, req, resp):
        try:
            media = await req.get_media()
            flow_id = media["id"]
            data = media["data"]
            all_function = data["all_function"]
            flow_name = data["flow_name"]

            prefect = PrefectService(
                flow_name,
                model_id="/home/ya/mapdata/safe/results/unsloth/llava-ov-7b-people-1208",
                image_input="/home/ya/mapdata/background.jpg",
                image_data=None
            )

            for function in all_function:
                task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
                prefect.append_task(task)

            back = prefect.run()

            resp.body = json.dumps(ResponEntity().ok(
                "测试流程成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("测试流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("测试流程失败", e))
            resp.status = falcon.HTTP_500


# 流程调用接口
class RunFlowController(PrefectController):
    async def on_post(self, req, resp):
        try:
            media = await req.get_media()
            flow_id = media["id"]
            data = media["data"]
            all_function = data["all_function"]
            flow_name = data["flow_name"]
            image_data = media["image_data"]

            prefect = PrefectService(
                flow_name,
                model_id="/home/ya/mapdata/safe/results/unsloth/llava-ov-7b-people-1208",
                image_input="/home/ya/mapdata/background.jpg",
                image_data=image_data
            )

            for function in all_function:
                task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
                prefect.append_task(task)

            back = prefect.run()

            resp.body = json.dumps(ResponEntity().ok(
                "测试流程成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("测试流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("测试流程失败", e))
            resp.status = falcon.HTTP_500


# 图片处理控件调用接口
class ImageProcessingFlowRunController(PrefectController):
    async def on_post(self, req, resp):
        try:
            # 统一接口参数
            media = await req.get_media()
            input_type = media["input_type"]
            input_data = media["input_data"]
            output_type = media["output_type"]
            flow_id = media["flow_id"]

            # 根据流程ID 获取流程和任务参数
            yaml_path = f"/home/ya/mapdata/flow/{flow_id}.yaml"
            yaml_data = PrefectDealService().parse_flow_yaml(yaml_path=yaml_path)
            # 解析yaml流程文件，并将所有的过程放进去

            prefect = PrefectService(
                yaml_data["flow_name"],
                **input_data
                # input_type=input_type,
                # input_data=input_data,
                # output_type=output_type
            )

            all_function = yaml_data["all_function"]
            for function in all_function:
                task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
                prefect.append_task(task)

            back = prefect.run()

            output_data = OutputData()
            output_data.text = back["text"]
            output_data.voice = back["voice_data"]

            resp.body = json.dumps(ResponEntity().ok(
                "图片处理控件调用接口成功",
                {
                    "output_type": output_type,
                    "output_data": output_data.to_dict()
                }
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("图片处理控件调用接口失败", e)
            resp.body = json.dumps(ResponEntity().exception("图片处理控件调用接口失败", e))
            resp.status = falcon.HTTP_500


# 聊天语音控件调用接口
class ChatVoiceFlowRunController(PrefectController):
    async def on_post(self, req, resp):
        try:
            # 统一接口参数
            media = await req.get_media()
            input_type = media["input_type"]
            input_data = media["input_data"]
            output_type = media["output_type"]
            flow_id = media["flow_id"]

            # 根据流程ID 获取流程和任务参数
            yaml_path = f"/home/ya/mapdata/flow/{flow_id}.yaml"
            yaml_data = PrefectDealService().parse_flow_yaml(yaml_path=yaml_path)
            # 解析yaml流程文件，并将所有的过程放进去

            prefect = PrefectService(
                yaml_data["flow_name"],
                **input_data
                # input_type=input_type,
                # input_data=input_data,
                # output_type=output_type
            )

            all_function = yaml_data["all_function"]
            for function in all_function:
                task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
                prefect.append_task(task)

            back = prefect.run()

            output_data = OutputData()
            output_data.text = back["text"]
            output_data.voice = back["voice_data"]

            resp.body = json.dumps(ResponEntity().ok(
                "聊天语音控件调用接口成功",
                {
                    "output_type": output_type,
                    "output_data": output_data.to_dict()
                }
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("聊天语音控件调用接口失败", e)
            resp.body = json.dumps(ResponEntity().exception("聊天语音控件调用接口失败", e))
            resp.status = falcon.HTTP_500


# 全局检索控件调用接口
class GlobalSearchFlowRunController(PrefectController):
    async def on_post(self, req, resp):
        try:
            # 统一接口参数
            media = await req.get_media()
            input_type = media["input_type"]
            input_data = media["input_data"]
            output_type = media["output_type"]
            flow_id = media["flow_id"]

            # # 根据流程ID 获取流程和任务参数
            # yaml_path = f"/home/ya/mapdata/flow/{flow_id}.yaml"
            # yaml_data = PrefectDealService().parse_flow_yaml(yaml_path=yaml_path)
            # # 解析yaml流程文件，并将所有的过程放进去
            #
            # prefect = PrefectService(
            #     yaml_data["flow_name"],
            #     **input_data
            #     # input_type=input_type,
            #     # input_data=input_data,
            #     # output_type=output_type
            # )
            #
            # all_function = yaml_data["all_function"]
            # for function in all_function:
            #     task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
            #     prefect.append_task(task)
            #
            # back = prefect.run()

            output_data = OutputData()
            # output_data.text = back["text"]
            # output_data.voice = back["voice_data"]

            output_data.image_list = []

            folder_path = "/home/ya/mapdata/camera_img"

            # 遍历文件夹中的所有文件
            for file_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, file_name)

                # 以二进制方式打开图像文件
                with open(image_path, "rb") as img_file:
                    img_data = img_file.read()

                # 对图像数据进行Base64编码
                base64_str = base64.b64encode(img_data).decode("utf-8")
                output_data.image_list.append(base64_str)

            resp.body = json.dumps(ResponEntity().ok(
                "全局检索控件调用接口成功",
                {
                    "output_type": output_type,
                    "output_data": output_data.to_dict()
                }
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("全局检索控件调用接口失败", e)
            resp.body = json.dumps(ResponEntity().exception("全局检索控件调用接口失败", e))
            resp.status = falcon.HTTP_500


# 文本处理控件调用接口
class TextProcessingFlowRunController(PrefectController):
    async def on_post(self, req, resp):
        try:
            # 统一接口参数
            input_type = req.media["input_type"]
            input_data = req.media["input_data"]
            output_type = req.media["output_type"]
            flow_id = req.media["flow_id"]

            # # 根据流程ID 获取流程和任务参数
            # yaml_path = f"/home/ya/mapdata/flow/{flow_id}.yaml"
            # yaml_data = PrefectDealService().parse_flow_yaml(yaml_path=yaml_path)
            # # 解析yaml流程文件，并将所有的过程放进去
            #
            # prefect = PrefectService(
            #     yaml_data["flow_name"],
            #     **input_data
            #     # input_type=input_type,
            #     # input_data=input_data,
            #     # output_type=output_type
            # )
            #
            # all_function = yaml_data["all_function"]
            # for function in all_function:
            #     task = TaskNode(function["function_name"], function["http_url"], function["parameters"], None, None)
            #     prefect.append_task(task)
            #
            # back = prefect.run()

            output_data = OutputData()
            # output_data.text = back["text"]
            # output_data.voice = back["voice_data"]

            output_data.image_list = []

            folder_path = "/home/ya/mapdata/camera_img"

            # 遍历文件夹中的所有文件
            for file_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, file_name)

                # 以二进制方式打开图像文件
                with open(image_path, "rb") as img_file:
                    img_data = img_file.read()

                # 对图像数据进行Base64编码
                base64_str = base64.b64encode(img_data).decode("utf-8")
                output_data.image_list.append(base64_str)

            resp.body = json.dumps(ResponEntity().ok(
                "全局检索控件调用接口成功",
                {
                    "output_type": output_type,
                    "output_data": output_data.to_dict()
                }
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("全局检索控件调用接口失败", e)
            resp.body = json.dumps(ResponEntity().exception("全局检索控件调用接口失败", e))
            resp.status = falcon.HTTP_500


def get_single_gstreamer_pipeline():
    gs_config_id = "e072466d-74f0-49db-951b-1e8d2453ead9"
    yaml_path = f"/home/ya/mapdata/gstreamer_yaml/cbtai/{gs_config_id}.yaml"
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
    return gs_piepline_config

def get_from_bpmn():
    # 默认使用的文件地址
    bpmn_file_path = "/home/ya/mapdata/flow_bpmn/cbtai/Process_1.bpmn"
    # 获取bpmn原始数据
    bpmn_parse_data = parse_bpmn_and_params(bpmn_file_path)
    # 获取bpmn实体类数据
    bpmn_entity = parsed_data_to_entity(bpmn_parse_data)
    # 获取模型接口数据
    model_infos = CbtModelFile().scanModelDir()
    # 遍历用户任务，为每一个任务加上其他需要的参数和访问的路径
    for user_task in bpmn_entity["user_tasks"]:
        model_id = user_task["model_id"]
        interface_id = str(user_task["interface_id"])
        model_interface_need = next(
            (interface for model_info in model_infos if model_info["model_id"] == model_id
             for interface in model_info["model_interfaces"] if str(interface["id"]) == interface_id),
            None
        )
        if model_interface_need:
            user_task["api_endpoint"] = f'http://{config.host}{model_interface_need["api_endpoint"]}'
            # user_task["parameters"] = model_interface_need["parameters"]
            in_comes = int(model_interface_need["in_comes"])
            req_comes = model_interface_need["req_comes"]
            for idx, req_come in enumerate(req_comes):
                if idx != in_comes:
                    user_task["up_params_parsed"].append(req_come)
            # 取出第一个元素
            first_element = user_task["up_params_parsed"].pop(0)

            # 插入到指定的位置
            user_task["up_params_parsed"].insert(in_comes, first_element)
        else:
            raise ValueError(f"未找到用户任务 {user_task['task_id']} 的匹配模型接口配置")
    return bpmn_entity


# 根据管道的输入、输出、流程的yaml文件，执行prefect流程
class GstreamerBpmnFlowRunController(PrefectController):
    async def on_get(self, req, resp):
        try:
            # 获取管道的输入和输出
            gs_piepline_config = get_single_gstreamer_pipeline()
            # 获取bpmn的流程
            bpmn_entity = get_from_bpmn()

            come_data_item = []
            for data in gs_piepline_config.gs_comes:
                come_data_item.append(DataItem(DaType(str(data["type"])), DaFormat(str(data["format"])), data["content"]))

            gos_data_item = []
            for data in gs_piepline_config.gs_gos:
                gos_data_item.append(DataItem(DaType(str(data["type"])), DaFormat(str(data["format"])), data["content"]))

            param_data = ReqParameter(come_data_item, gos_data_item, [])

            # 获取一张图的base64编码
            img_path = "/home/ya/mapdata/true.jpeg"
            # 读取图像
            img = cv2.imread(img_path)
            # 将图像从BGR转为RGB（OpenCV默认是BGR格式）
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 将图像转换为JPEG格式的字节数据
            _, buffer = cv2.imencode('.jpg', img_rgb)
            # 将字节数据编码为base64字符串
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            for data in param_data.gs_input_data:
                data.data = img_base64

            flow_back = PrefectRun(bpmn_entity, param_data)

            back = []
            for data in flow_back.gs_output_data:
                back.append(data.obj2dct())

            resp.body = json.dumps(ResponEntity().ok(
                "根据管道的输入、输出、流程的yaml文件，执行prefect流程成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("根据管道的输入、输出、流程的yaml文件，执行prefect流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("根据管道的输入、输出、流程的yaml文件，执行prefect流程失败", e))
            resp.status = falcon.HTTP_500

# 测试运行语音翻译管道
class TextTranslateController(PrefectController):
    async def on_get(self, req, resp):
        try:
            dealVoicePipeline = DealVoicePipeline()
            dealVoicePipeline.start()

            resp.body = json.dumps(ResponEntity().ok(
                "测试运行语音翻译管道成功",
                "123"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("测试运行语音翻译管道失败", e)
            resp.body = json.dumps(
                ResponEntity().exception("测试运行语音翻译管道失败", e))
            resp.status = falcon.HTTP_500

