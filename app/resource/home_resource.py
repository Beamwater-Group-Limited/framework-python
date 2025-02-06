# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : home_resource.py
# @Author        : henryren
# @Time          : 2024/12/25 23:35
# @Function      : 
# @Desc          :
import traceback

import falcon

from app import config
from app.error.PyLogger import pyLogger
from app.model.cbt_flow_file import CbtFlowFile
from app.model.model.cbt_model_file import CbtModelFile
from app.model.model.cbt_model_info_dao import CbtModelInfoDao
from app.model.renderer_model import Jinja2Renderer

logger = pyLogger()


# 定义基础渲染类，用于渲染 Jinja2 模板的页面响应
class BasePage:
    def __init__(self, template_name, **kwargs):
        self.template_name = template_name
        self.context = kwargs
        # 定义模板的文件路径
        templates_path = config.basepath / 'templates'
        # 定义静态文件的URL路径
        static_url = 'static'
        # 创建Jinja2模板渲染器的实例，用于在后续渲染HTML页面时使用
        self.renderer = Jinja2Renderer(templates_path=templates_path, static_url=static_url)

    async def on_get(self, req, resp):
        print(req.params)
        # 设置HTTP响应状态为200（成功）
        resp.respon_status = falcon.HTTP_200
        # 设置响应类型为HTML
        resp.content_type = falcon.MEDIA_HTML
        # resp.content_type = 'text/html'
        # 将渲染后的HTML内容写入响应体
        resp.text = self.renderer.render(self.template_name, **self.context)


# 不同页面的具体实现
class MainPage(BasePage):
    def __init__(self):
        super().__init__('main.html', title='主页 - 欢迎光临', content='这是主页的内容区域，欢迎访问我们的网站。')


class AboutPage(BasePage):
    def __init__(self):
        super().__init__('main.html', title='关于我们', content='这是关于我们信息的页面。')


class ServicesPage(BasePage):
    def __init__(self):
        super().__init__('main.html', title='我们的服务', content='此页面介绍我们提供的服务内容。')


class ContactPage(BasePage):
    def __init__(self):
        super().__init__('main.html', title='联系我们', content='如果需要联系，请查看本页面信息。')


class ImageUploadPage(BasePage):
    def __init__(self):
        super().__init__('image_upload.html', title='首页', message='欢迎使用 Falcon 和 Jinja2 进行前后端统一开发！')


class ProductPage(BasePage):
    def __init__(self):
        super().__init__('product.html')


class ModelPage(BasePage):
    def __init__(self):
        super().__init__('models.html')
        self.cbtModelFile = CbtModelFile()

    async def on_get(self, req, resp):
        models = self.cbtModelFile.scanModelDir()
        context = {
            "models": models,
            "host": f'http://{config.host}'
        }
        resp.respon_status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        resp.text = self.renderer.render(self.template_name, **context)

class EditInterfacePage(BasePage):
    def __init__(self):
        self.cbtModelFile = CbtModelFile()
        self.models = None
        self.model_infos = None

        super().__init__('edit_interface.jinja2')

    async def on_get(self, req, resp):
        try:
            self.models = self.cbtModelFile.scanModelDir()
            self.model_infos = [CbtModelInfoDao.as_CbtModelInfo(diction) for diction in self.models]
            # 从请求中获取参数 model_id（模型ID），此参数为必填
            model_id = req.get_param('model_id', required=True)
            # 从请求中获取参数 interface_id（接口ID），转换为整数并进行必填验证
            interface_id = int(req.get_param('interface_id', required=True))

            # 查找模型列表中符合指定 model_id 的模型对象
            model = next(filter(lambda entry: entry.model_id== model_id, self.model_infos), None)

            if model:
                # 如果模型存在，继续查找模型对象中符合指定 interface_id 的接口对象
                interface = next(filter(lambda entry: entry.id == interface_id, model.model_interfaces), None)
                if interface:
                    interface_dct = interface.obj2dct()
                    # 如果接口存在，设置渲染模板中所需要的上下文数据
                    self.context = {
                        "interface": interface_dct,  # 接口对象
                        "model_id": model_id,  # 模型ID
                        "host": f'http://{config.host}'  # 服务器主机地址
                    }
                    # 设置响应状态为 200（成功）
                    resp.respon_status = falcon.HTTP_200
                    # 设置响应内容类型为 HTML
                    resp.content_type = falcon.MEDIA_HTML
                    # 使用模板渲染器渲染模板，并将渲染结果写入响应正文
                    resp.text = self.renderer.render(self.template_name, **self.context)
                else:
                    # 如果接口未找到，记录调试日志
                    logger.debug(f'接口为空 {interface_id}')
            else:
                # 如果模型未找到，记录调试日志
                logger.debug(f'模型为空 {model_id}')
        except Exception as e:
            # 定义模板的文件路径
            templates_path = config.basepath / 'templates'
            # 定义静态文件的URL路径
            static_url = 'static'
            error_details = traceback.format_exc()
            logger.error(f"{e}\n{error_details}")
            context = {
                'status_code': falcon.HTTP_500,
                'error_message': f'{e}',
                'error_details': f'{error_details}'
            }
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_HTML
            resp.text = Jinja2Renderer(templates_path=templates_path, static_url=static_url).render('error.jinja2',
                                                                                                    **context)

    # 增加一个处理 POST 请求的方法，用于保存接口修改后的内容
    async def on_post(self, req, resp):
        req_data = await req.get_media()
        # 提取 POST 请求中的数据
        interface_id = int(req_data.get('interface_id'))
        model_id = req_data.get('model_id')
        interface_name = req_data.get('interface_name')
        api_endpoint = req_data.get('api_endpoint' )
        headers = req_data.get('headers' )
        method = req_data.get('method')
        request_body_json = req_data.get('request_body_json' )
        response_json = req_data.get('response_json')
        # 返回成功消息
        resp.status = falcon.HTTP_200
        resp.text = "接口更新成功"

class PreFectFlowPage(BasePage):
    def __init__(self):
        # 模拟数据
        func_options = [
            {"value": "func1", "label": "Function 1"},
            {"value": "func2", "label": "Function 2"},
        ]
        current_node = {
            "nodeId": "123",
            "params": [{"key": "param1", "default_value": "value1"}],
            "functionName": "func1",
        }
        configure = {
            "show": False,
            "id": "",
            "currentNode": current_node,
            "funcOptions": func_options,
            "visible": False,
            "funcList": []
        }
        super().__init__('prefect_flow.html', **configure)


class FlowListPage(BasePage):
    def __init__(self):
        super().__init__('flow_list.html')
    async def on_get(self, req, resp):
        cbtFlowFile = CbtFlowFile(config.ORGANIZATION)
        flows = cbtFlowFile.scanFlowYamlDir()
        context = {
            "processes": flows,
            "pagination": {
                "current_page": 0,
                "total_pages": len(flows),
                "is_first_page": False,
                "is_last_page": False,
            }
        }
        resp.respon_status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        resp.text = self.renderer.render(self.template_name, **context)


class BpmnEditorPage(BasePage):
    def __init__(self):
        configure = {
        }
        super().__init__('bpmn_editor.html', **configure)
