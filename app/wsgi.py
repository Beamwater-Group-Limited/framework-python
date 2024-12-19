# !/usr/bin/env/python
import logging

import falcon
import sys
import os

from app import config
from app.controller.config_controller import GetAllFunctionController, SaveFlowController, GetAllFlowController, \
    GetFlowByIdController, SaveImgDataController, ComponentToFlowController, GetComponentToFlowListController
from app.controller.prefect_controller import TestRunFlowController, RunFlowController, \
    ImageProcessingFlowRunController, ChatVoiceFlowRunController, GlobalSearchFlowRunController

current_dir = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_dir)[0]
sys.path.append(rootPath)

from falcon_cors import CORS
from app.controller.helloworld_controller import HelloWorldController

logger = logging.getLogger(config.app_name)
# 配置日志模块的信息标准【什么等级的信息会被捕捉】
logger.setLevel(config.log_level)
# 配置日志模块的处理器【处理日志模块捕捉到的等级】
logger.addHandler(logging.StreamHandler())


def create_app():
    helloWordController = HelloWorldController()
    getAllFunctionController = GetAllFunctionController()
    saveFlowController = SaveFlowController()
    getAllFlowController = GetAllFlowController()
    testRunFlowController = TestRunFlowController()
    getFlowByIdController = GetFlowByIdController()
    saveImgDataController = SaveImgDataController()
    runFlowController = RunFlowController()
    imageProcessingFlowRunController = ImageProcessingFlowRunController()
    chatVoiceFlowRunController = ChatVoiceFlowRunController()
    globalSearchFlowRunController = GlobalSearchFlowRunController()
    componentToFlowController = ComponentToFlowController()
    getComponentToFlowListController = GetComponentToFlowListController()

    cors = CORS(
        allow_origins_list=['http://localhost:8080', 'http://localhost:8082'],
        allow_all_origins=True,
        allow_credentials_all_origins=True,
        allow_all_methods=True,
        allow_all_headers=True,
    )

    # api = falcon.API()
    api = falcon.API(middleware=[cors.middleware])
    api.add_route("/helloWorld", helloWordController)

    # 获取所有功能项
    api.add_route('/v1/get_all_function', getAllFunctionController)

    # 流程保存
    api.add_route('/v1/save_flow', saveFlowController)
    # 获取所有的流程
    api.add_route('/v1/get_all_flow', getAllFlowController)
    # 根据流程id获取流程
    api.add_route('/v1/get_flow_by_id', getFlowByIdController)
    # 测试运行某一个流程
    api.add_route('/v1/test_run_flow', testRunFlowController)
    # 运行某一个流程
    api.add_route('/v1/run_flow', runFlowController)

    # 根据图像数据上传图像
    api.add_route('/v1/save_img_data', saveImgDataController)

    # 图像处理控件调用接口
    api.add_route('/v1/image_processing_flow_run', imageProcessingFlowRunController)
    # 聊天语音控件调用接口
    api.add_route('/v1/chat_voice_flow_run', chatVoiceFlowRunController)
    # 全局搜索控件调用接口
    api.add_route('/v1/global_search_flow_run', globalSearchFlowRunController)

    # 控件绑定流程
    api.add_route('/v1/component_to_flow', componentToFlowController)
    # 获取控件绑定流程列表
    api.add_route('/v1/get_component_to_flow_list', getComponentToFlowListController)

    return api


app = create_app()
