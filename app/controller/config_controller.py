import logging
import os

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
            resp.body = json.dumps(ResponEntity().ok(
                "获取所有的功能项成功",
                [
                    {
                        "name": "测试大模型类型1",
                        "value": [
                            {
                                "function_name": "详细描述",
                                "http_url": "http://192.168.0.70:28486/v1/inferenceController",
                                "parameters": [
                                    {
                                        "key": "text",
                                        "default_value": "## 任务说明\n对给定的监控画面,进行详细分析与描述。\n\n### 分析要求\n1. **描述侧重点**：可以侧重异常分析，对画面中存在的异常现象进行深入分析。  \n2. **描述要求**：\n   - 必须基于画面中清晰可见的事实对异常进行描述。不得添加画面中无法确认的信息。\n    - 异常对象（如人员、车辆、设施）的外观、位置、行为特征。  \n    - 异常行为可能造成的安全影响或后果。  \n    - 对异常出现的原因与背景进行逻辑分析和推理，但不能使用“可能”、“或许”、“似乎”等模棱两可的词语。  \n    - 描述需条理清晰、逻辑完整，并保证文字流畅可读。  \n   - 字数要求：至少**80字**。\n   - 请使用严谨的叙述口吻，避免过度揣测和不确定性描述。\n\n3. **输出格式要求**：\n   - 输出为一个 txt文本。  \n   - 详细描述（中文）。  \n\n4. **返回格式示例**\n   请参考以下 txt 文本格式示例（此为格式参考）：\n   ```txt\n   \"这里是详细描述内容，80字以上。\"\n   ```\n\n### 最终要求\n- 描述需在80字以上。\n- 遵守上述所有要求并自我检查回答的合理性和完备性。\n",
                                        "is_empty": "0",
                                        "is_update": "1"
                                    },
                                    {
                                        "key": "image_data",
                                        "default_value": "",
                                        "is_empty": "1",
                                        "is_update": "1"
                                    },
                                    {
                                        "key": "model_id",
                                        "default_value": "/home/ya/mapdata/safe/results/unsloth/llava-ov-7b-people-1208",
                                        "is_empty": "0",
                                        "is_update": "0"
                                    }
                                ]
                            },
                            {
                                "function_name": "异常类型检测",
                                "http_url": "http://192.168.0.70:28486/v1/inferenceController",
                                "parameters": [
                                    {
                                        "key": "text",
                                        "default_value": "## 任务说明\n请对给定的监控图像进行全面分析。你的目标是识别下列所有可能的异常情况，而不仅仅是某一个类型。\n### 需要识别的异常类型分为4大类，需要从4大类中的具体异常类型中精确选择 `type` 值\n**1人员 (异常人员数组)**：\n- 无安全防护装备\n- 服装不符合要求\n- 违规行为/打电话,吸烟\n- 操作危险工具\n- 人员攀爬\n**2车辆 (异常车辆数组)**：\n- 未授权车辆进入\n- 车辆违规闯入\n**3物资 (异常物资数组)**：\n- 设施损坏\n- 油料泄漏\n**4环境 (环境危害数组)**：\n- 火光或烟雾\n### 要求\n1. **全面检查**：请逐一对上述所有类型进行检视。若图像中存在任一异常情况，请在对应数组中加入一条记录。\n2. **无异常则为空**：如该类异常不存在，请确保对应的数组为空。\n3. **type字段取值严格限制**：\n   - `type` 字段的值必须是上述定义的对应类型列表中其中一个。\n   - 不得使用未定义的词汇作为 `type` 值，也不得使用上位类别名（如“人员”）代替具体类型。\n4. **JSON输出结构**：请严格按照下方给定的 JSON 示例回答。不得省略任意一个键，即使为空数组也要保留。\n   - `type`字段的值必须从上面定义的类型数组中精确选择。\n\n### 返回格式示例\n请参考以下 JSON 格式。若有异常则在相应数组中填入一条，每条记录包含：\n- `type`: 从上述定义的类型中选择一个（必须精确匹配给定类型）\n\n```json\n{\n  \"人员\": [\n    {\n      \"type\": \"\"\n    }\n  ],\n  \"车辆\": [],\n  \"资源\": [],\n  \"环境\": []\n}\n```\n\n### 最终要求\n- 对图像中的所有元素进行全面识别：如有人无安全装备就写入\"人员\"数组；如有车辆闯入就写入\"车辆\"数组；以此类推。\n- 若某类异常不存在，则对应数组需为空。\n- 严格使用上述给定的类型名称作为 `type` 的取值，不得使用其他名称。\n\n请根据以上要求输出最终的 JSON 格式结果。\n",
                                        "is_empty": "0",
                                        "is_update": "1"
                                    },
                                    {
                                        "key": "image_data",
                                        "default_value": "",
                                        "is_empty": "1",
                                        "is_update": "1"
                                    },
                                    {
                                        "key": "model_id",
                                        "default_value": "/home/ya/mapdata/safe/results/unsloth/llava-ov-7b-people-1208",
                                        "is_empty": "0",
                                        "is_update": "0"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "手写体识别",
                        "value": [
                            {
                                "function_name": "手写体识别",
                                "http_url": "http://192.168.0.70:28486/v1/mlpInference",
                                "parameters": [
                                    {
                                        "key": "image_data",
                                        "default_value": "",
                                        "is_empty": "0",
                                        "is_update": "1"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "图文检索",
                        "value": [
                            {
                                "function_name": "图文检索",
                                "http_url": "http://192.168.0.70:28586/v1/searchController",
                                "parameters": []
                            }
                        ]
                    },
                    {
                        "name": "文字转语音",
                        "value": [
                            {
                                "function_name": "文字转语音",
                                "http_url": "http://192.168.0.70:28686/v1/ttsController",
                                "parameters": [
                                    {
                                        "key": "text",
                                        "default_value": "",
                                        "is_empty": "0",
                                        "is_update": "1"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "asr",
                        "value": [
                            {
                                "function_name": "asr",
                                "http_url": "http://192.168.0.70:28686/v1/asrController",
                                "parameters": []
                            }
                        ]
                    }
                ]
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
