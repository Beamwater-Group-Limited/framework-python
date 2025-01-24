import logging

import falcon
import simplejson as json
import yaml

from app import config
from app.entity.respon_entity import ResponEntity
from app.model.model.cbt_model_file import CbtModelFile
from app.model.parsed_bpmn.bpmn_entity import parsed_data_to_entity
from app.model.parsed_bpmn.bpmn_parser import parse_bpmn_and_params

logger = logging.getLogger(config.app_name)


class BpmnYamlController:
    def __init__(self):
        pass


# 从bpmn文件中获取到flow可运行的yaml数据
class BpmnToYamlDataController(BpmnYamlController):
    async def on_get(self, req, resp):
        try:
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
                else:
                    raise ValueError(f"未找到用户任务 {user_task['task_id']} 的匹配模型接口配置")

            # 将结果保存到yaml文件中
            yaml_file_path = "/home/ya/mapdata/flow_yaml/cbtai/bpmn_to_yaml_test.yaml"
            with open(yaml_file_path, 'w', encoding='utf-8') as file:
                # 使用 yaml.safe_dump 方法将数据转换成 YAML 格式
                yaml.safe_dump(bpmn_entity, file, allow_unicode=True)

            resp.body = json.dumps(ResponEntity().ok(
                "从bpmn文件中获取到flow可运行的yaml数据成功",
                bpmn_entity
            ))
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.error("从bpmn文件中获取到flow可运行的yaml数据失败", exc_info=True)
            resp.body = json.dumps(ResponEntity().exception(
                "从bpmn文件中获取到flow可运行的yaml数据失败",
                str(e)
            ))
            resp.status = falcon.HTTP_500