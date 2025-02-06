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

    # 初始化方法，用于设置模板路径和静态文件URL路径
    def __init__(self, templates_path: str = None, static_url: str = None):
        if templates_path is None:
            templates_path = config.basepath / 'templates'
        if static_url is None:
            static_url = config.basepath / '/static/'
        # 输出日志，记录模板路径的绝对路径
        logger.debug(f"模板路径:{os.path.abspath(templates_path)}")
        # 配置Jinja2的环境，指定加载器为FileSystemLoader，加载模板路径
        # 同时开启HTML和XML文件的自动转义
        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml', 'htm', 'jinja2'])
        )
        # 可以在此配置一些 Jinja2 filters 或 global functions
        self.env.filters['format_date'] = lambda d: d.strftime('%Y-%m-%d')
        # 全局函数
        # self.env.globals['some_global'] = ...
        # 初始化静态文件的URL路径
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
