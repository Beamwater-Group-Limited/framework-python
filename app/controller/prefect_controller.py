import base64
import logging
import os

import simplejson as json
import falcon

from app import config
from app.entity.output_data import OutputData
from app.entity.respon_entity import ResponEntity
from app.entity.task_node import TaskNode
from app.service.prefect_service import PrefectService, PrefectDealService

logger = logging.getLogger(config.app_name)


class PrefectController:
    def __init__(self):
        pass


# 测试流程
class TestRunFlowController(PrefectController):
    def on_post(self, req, resp):
        try:
            flow_id = req.media["id"]
            data = req.media["data"]
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
    def on_post(self, req, resp):
        try:
            flow_id = req.media["id"]
            data = req.media["data"]
            all_function = data["all_function"]
            flow_name = data["flow_name"]
            image_data = req.media["image_data"]

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
    def on_post(self, req, resp):
        try:
            # 统一接口参数
            input_type = req.media["input_type"]
            input_data = req.media["input_data"]
            output_type = req.media["output_type"]
            flow_id = req.media["flow_id"]

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
    def on_post(self, req, resp):
        try:
            # 统一接口参数
            input_type = req.media["input_type"]
            input_data = req.media["input_data"]
            output_type = req.media["output_type"]
            flow_id = req.media["flow_id"]

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
    def on_post(self, req, resp):
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


# 文本处理控件调用接口
class TextProcessingFlowRunController(PrefectController):
    def on_post(self, req, resp):
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
