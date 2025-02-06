# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : webpack_resource.py
# @Author        : henryren
# @Time          : 2024/12/25 23:35
# @Function      : 
# @Desc          :

import falcon

from app import config
from app.error.PyLogger import pyLogger
from app.model.renderer_model import Jinja2Renderer

logger = pyLogger()
# 定义基础渲染类，用于渲染 Jinja2 模板的页面响应
class BaseWebpackPage:
    def __init__(self, template_name, **kwargs):
        self.template_name = template_name
        self.context = kwargs
        self.template_file = f'{self.template_name}.jinja2'
        # 定义模板的文件路径
        templates_path = config.basepath / 'templates/'
        # 定义静态文件的URL路径
        static_url = f'static/{self.template_name}'
        # 创建Jinja2模板渲染器的实例，用于在后续渲染HTML页面时使用
        self.renderer = Jinja2Renderer(templates_path=templates_path, static_url=static_url)

    async def on_get(self, req, resp):
        print(req.params)
        # 设置HTTP响应状态为200（成功）
        resp.respon_status = falcon.HTTP_200
        # 设置响应类型为HTML
        resp.content_type = falcon.MEDIA_HTML
        resp.text = self.renderer.render(self.template_file, **self.context)


class BpmnjsWebpackPage(BaseWebpackPage):
    def __init__(self):
        configure = {
            'user' : {'name': 'Alice', 'roles': ['admin', 'editor']}
        }
        super().__init__('bpmn-js-example-properties-panel', **configure)

class PropertiesPanelAsyncExtensionPage(BaseWebpackPage):
    def __init__(self):
        configure = {
            'da': {
                "apiUrl": f"http://{config.host}",
                "shouldFetchData": True,
                "flowId": "Process_1",
                "userId": "cbtai",
            },
            'user': {'name': 'Alice', 'roles': ['admin', 'editor']}
        }
        super().__init__('properties-panel-async-extension', **configure)