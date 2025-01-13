# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : home_resource.py
# @Author        : henryren
# @Time          : 2024/12/25 23:35
# @Function      : 
# @Desc          :
import falcon

from app.model.renderer_model import Jinja2Renderer


# 定义基础渲染类，用于渲染 Jinja2 模板的页面响应
class BasePage:
    def __init__(self, template_name, **kwargs):
        self.template_name = template_name
        self.context = kwargs

    async def on_get(self, req, resp):
        try:
            print(req.params)
            # 创建Jinja2模板渲染器的实例，用于在后续渲染HTML页面时使用
            renderer = Jinja2Renderer()
            # 根据模板名称和上下文数据渲染HTML页面
            html = renderer.render(self.template_name, **self.context)
        except Exception as e:
            print(e)
        # 设置HTTP响应状态为200（成功）
        resp.status = falcon.HTTP_200
        # 设置响应类型为HTML
        resp.content_type = falcon.MEDIA_HTML
        # resp.content_type = 'text/html'
        # 将渲染后的HTML内容写入响应体
        resp.text = html


# 视频流显示页面
class VideoMonitoringPage(BasePage):
    def __init__(self):
        super().__init__('video_monitoring_page.html',
                         stream='rtsp://admin:yuanm201109@192.168.0.112:554/cam/realmonitor?channel=1&subtype=0')


# 视频流配置页面
class ConfigPageTemplate(BasePage):
    def __init__(self):
        super().__init__('config_page_template.html',
                         stream='rtsp://admin:yuanm201109@192.168.0.112:554/cam/realmonitor?channel=1&subtype=0')


# 摄像头使用页面
class VideoPageUse(BasePage):
    def __init__(self):
        super().__init__('video_monitoring_page_template_styles.html', stream='rtsp://192.168.0.70:8554/kaifaban')


# 摄像头配置页面
class VideoConfig(BasePage):
    def __init__(self):
        super().__init__('video_config.html')


# Gstreamer流运行配置页面
class FlowRunConfig(BasePage):
    def __init__(self):
        super().__init__('flow_run_config.html')


class ProductPage(BasePage):
    def __init__(self):
        super().__init__('product.html')
