import logging
import os

import requests
import simplejson as json
import falcon
from app import config
import uuid
import numpy as np
import cv2
import yaml
import base64

from app.entity.respon_entity import ResponEntity

logger = logging.getLogger(config.app_name)


class ConfigController:
    def __init__(self):
        pass


# 获取所有的功能项
class GetAllFunctionController(ConfigController):
    def on_get(self, req, resp):
        try:
            # 调用接口返回数据
            url = f"http://{config.baseurl}:28486/v1/functionGetController"
            # 调用请求，并传值
            response = requests.post(url)
            json_string = response.content.decode('utf-8')
            # 将字符串解析为 JSON 对象
            json_data = json.loads(json_string)
            back = json_data['data']
            resp.body = json.dumps(ResponEntity().ok(
                "获取所有的功能项成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取所有的功能项失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取所有的功能项失败", e))
            resp.status = falcon.HTTP_500


# 流程保存
class SaveFlowController(ConfigController):
    def on_post(self, req, resp):
        try:
            all_function = req.media["all_function"]
            flow_name = req.media["flow_name"]

            yaml_id = str(uuid.uuid4())

            yaml_path = f"/home/ya/mapdata/flow/{yaml_id}.yaml"
            yaml_content = {"flow_name": flow_name, "all_function": all_function}

            with open(yaml_path, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump(yaml_content, file)

            resp.body = json.dumps(ResponEntity().ok(
                "流程保存成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("流程保存失败", e)
            resp.body = json.dumps(ResponEntity().exception("流程保存失败", e))
            resp.status = falcon.HTTP_500


# 获取所有的流程
class GetAllFlowController(ConfigController):
    def on_post(self, req, resp):
        try:

            yaml_folder = f"/home/ya/mapdata/flow"

            files = []
            for root, _, filenames in os.walk(yaml_folder):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            back = []
            for yaml_path in files:
                # 如果文件已存在，读取文件中的内容
                flow_id = os.path.splitext(os.path.basename(yaml_path))[0]
                with open(yaml_path, 'r') as file:
                    existing_data = yaml.safe_load(file)
                    back.append({
                        "id": flow_id,
                        "data": existing_data
                    })

            resp.body = json.dumps(ResponEntity().ok(
                "获取所有的流程成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取所有的流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取所有的流程失败", e))
            resp.status = falcon.HTTP_500


# 根据流程id获取流程
class GetFlowByIdController(ConfigController):
    def on_post(self, req, resp):
        try:
            flow_id = req.media["flow_id"]
            yaml_path = f"/home/ya/mapdata/flow/{flow_id}.yaml"

            with open(yaml_path, 'r') as file:
                existing_data = yaml.safe_load(file)

            resp.body = json.dumps(ResponEntity().ok(
                "根据流程id获取流程成功",
                {
                    "id": flow_id,
                    "data": existing_data
                }
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("根据流程id获取流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("根据流程id获取流程失败", e))
            resp.status = falcon.HTTP_500


# 根据图像流将图像保存到指定的位置
class SaveImgDataController(ConfigController):
    def on_post(self, req, resp):
        try:
            file = req.media["file"]
            if file is None:
                raise ValueError("未找到上传文件")

            # 第一步：解码 Base64 字符串
            img_data = base64.b64decode(file)
            # 第二步：将字节数据转换为 NumPy 数组
            nparr = np.frombuffer(img_data, np.uint8)
            # 第三步：将 NumPy 数组转换为 OpenCV 图像格式
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_id = str(uuid.uuid4())
            file_path = os.path.join(f"/home/ya/mapdata/upload_file/{img_id}.jpg")
            # 使用 OpenCV 保存图像
            cv2.imwrite(file_path, img)

            resp.body = json.dumps(ResponEntity().ok(
                "根据图像流将图像保存到指定的位置成功",
                file_path
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("根据图像流将图像保存到指定的位置失败", e)
            resp.body = json.dumps(ResponEntity().exception("根据图像流将图像保存到指定的位置失败", e))
            resp.status = falcon.HTTP_500


# 控件绑定流程
class ComponentToFlowController(ConfigController):
    def on_post(self, req, resp):
        try:
            save_data = req.media["data"]
            yaml_file = "/home/ya/mapdata/component_to_flow.yaml"

            # 从文件加载现有数据
            data = []
            if os.path.exists(yaml_file):
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

            component_found = False
            for entry in save_data:
                for i, item in enumerate(data):
                    if item.get('component') == entry['component']:
                        # 找到已有组件则更新
                        data[i] = entry
                        component_found = True
                        break

                # 如果不存在则追加
                if not component_found:
                    data.append(entry)
                component_found = False

            with open(yaml_file, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump(data, file)
            resp.body = json.dumps(ResponEntity().ok(
                "控件绑定流程成功",
                "success"
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("控件绑定流程失败", e)
            resp.body = json.dumps(ResponEntity().exception("控件绑定流程失败", e))
            resp.status = falcon.HTTP_500


# 获取控件绑定流程列表
class GetComponentToFlowListController(ConfigController):
    def on_post(self, req, resp):
        try:
            yaml_file = "/home/ya/mapdata/component_to_flow.yaml"
            back = []
            if os.path.exists(yaml_file):
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    back = yaml.safe_load(f)
            resp.body = json.dumps(ResponEntity().ok(
                "获取控件绑定流程列表成功",
                back
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("获取控件绑定流程列表失败", e)
            resp.body = json.dumps(ResponEntity().exception("获取控件绑定流程列表失败", e))
            resp.status = falcon.HTTP_500
