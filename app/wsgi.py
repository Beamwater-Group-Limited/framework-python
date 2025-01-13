# !/usr/bin/env/python

from gi.repository import Gst, GObject, GLib
Gst.init(None)
import logging

import sys
import os

import falcon

from app import config
from app.controller.config_controller import GetAllFunctionController, SaveFlowController, GetAllFlowController, \
    GetFlowByIdController, SaveImgDataController, ComponentToFlowController, GetComponentToFlowListController
from app.controller.gstreamer_controller import GetAllGstreamerController, AddGstreamerController, \
    PauseGstreamerController, UpdateGstreamerProcessMountController, SendVoiceController
from app.controller.home_resource import VideoMonitoringPage, ConfigPageTemplate, VideoPageUse, VideoConfig, \
    GstreamerConfig
from app.controller.prefect_controller import TestRunFlowController, RunFlowController, \
    ImageProcessingFlowRunController, ChatVoiceFlowRunController, GlobalSearchFlowRunController
from falcon.asgi import App

from app.controller.video_controller import AddInputCameraController, GetInputCameraController, \
    DelInputCameraController, UpdateInputCameraController

current_dir = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_dir)[0]
sys.path.append(rootPath)

from falcon_cors import CORS
from app.controller.helloworld_controller import HelloWorldController


sys.path.insert(0, './app')


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
    addInputCameraController = AddInputCameraController()
    getInputCameraController = GetInputCameraController()
    delInputCameraController = DelInputCameraController()
    updateInputCameraController = UpdateInputCameraController()
    getAllGstreamerController = GetAllGstreamerController()
    addGstreamerController = AddGstreamerController()
    pauseGstreamerController = PauseGstreamerController()
    updateGstreamerProcessMountController = UpdateGstreamerProcessMountController()
    sendVoiceController = SendVoiceController()

    cors = CORS(
        allow_origins_list=['http://localhost:8080', 'http://localhost:8082'],
        allow_all_origins=True,
        allow_credentials_all_origins=True,
        allow_all_methods=True,
        allow_all_headers=True
    )

    # api = falcon.API()
    # api = falcon.API(middleware=[cors.middleware])
    api = App(cors_enable=True)
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
    """
    video摄像头数据管理
    """
    # 获取所有摄像头数据
    api.add_route('/v1/getInputCameraController', getInputCameraController)
    # 添加摄像头
    api.add_route('/v1/addInputCameraController', addInputCameraController)
    # 删除摄像头数据
    api.add_route('/v1/delInputCameraController', delInputCameraController)
    # 修改摄像头数据
    api.add_route('/v1/updateInputCameraController', updateInputCameraController)
    """
    gstreamer流运行管理
    """
    # 获取gstreamer流运行
    api.add_route('/v1/getAllGstreamerController', getAllGstreamerController)
    # 添加gstreamer流运行
    api.add_route('/v1/addGstreamerController', addGstreamerController)
    # 暂停运行的流
    api.add_route('/v1/pauseGstreamerController', pauseGstreamerController)
    # 修改运行的流挂载的流程
    api.add_route('/v1/updateGstreamerProcessMountController', updateGstreamerProcessMountController)
    # 通过gstreamer播放声音
    api.add_route('/v1/sendVoiceController', sendVoiceController)

    return api

def rander_page(api:App)-> 'App':
    # 创建 HomeResource 的实例，用于处理主页的相关请求
    video_monitoring_page = VideoMonitoringPage()
    config_page_template = ConfigPageTemplate()
    video_page_use = VideoPageUse()
    videoConfig = VideoConfig()
    gstreamerConfig = GstreamerConfig()
    # 添加静态文件中间件
    api.add_static_route('/static', config.basepath / 'static')
    api.add_route('/video_monitoring_page', video_monitoring_page)
    api.add_route('/config_page_template', config_page_template)
    api.add_route('/video_page_use', video_page_use)
    api.add_route('/videoConfig', videoConfig)
    api.add_route('/gstreamerConfig', gstreamerConfig)


    return api

# 调用方法创建应用实例，赋值给变量 app
app = rander_page(create_app())
