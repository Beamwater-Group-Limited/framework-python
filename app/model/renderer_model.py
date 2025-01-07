# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : renderer.py
# @Author        : henryren
# @Time          : 2024/12/25 23:29
# @Function      : 
# @Desc          :
import json
import os
import traceback

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app import config
from app.error.PyLogger import pyLogger

logger = pyLogger()
# 定义一个Jinja2模板渲染器类
class Jinja2Renderer:
    # 初始化方法，设置模板路径和静态文件URL
    def __init__(self):
        templates_path  = config.basepath / 'templates'
        static_url = config.basepath / '/static/'
        logger.debug(f"模板路径:{os.path.abspath(templates_path)}")
        # 配置Jinja2环境，使用FileSystemLoader加载模板路径，并自动转义HTML和XML文件
        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml'])
        )
        # 设置静态文件URL路径
        self.static_url = static_url

    # 定义渲染方法，根据模板名称和上下文渲染模板
    def render(self, template_name, **context):
        try:
            # 根据模板名称获取模板对象
            template = self.env.get_template(template_name)
            # 在上下文中添加静态文件URL，方便模板文件中使用
            context['static_url'] = self.static_url
            # 渲染模板并返回渲染后的字符串
            return template.render(**context)
        except Exception as e:
            traceback.format_exc()
            logger.error(f"无法渲染模板：{e}\n{traceback.format_exc()}")