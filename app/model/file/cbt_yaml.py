# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_yaml.py
# @Author        : henryren
# @Time          : 2025/1/12 19:42
# @Function      : 
# @Desc          :
from pathlib import Path
from typing import Dict

import yaml
from app import config
from app.error.PyLogger import pyLogger
from app.error.PyTFError import catchexcept

logger = pyLogger()


class CbtYaml:
    # 初始化方法，用于设置存储 YAML 文件路径的属性
    def __init__(self, base_path: Path, relative_path: str):
        # YAML 文件存储目录路径，通常由基路径和业务相关信息组成
        self.yaml_cate = base_path
        # YAML 文件的相对路径，表示相对于基路径的文件路径
        self.yaml_relative_path = relative_path
        # YAML 文件的完整路径，基于存储目录路径和相对路径计算得出
        self.yaml_file_path = self.yaml_cate / relative_path
        # 从相对路径中提取组织名称，通常是路径的第一级目录
        self.organize_name = relative_path.split('/')[0]
        # 从相对路径中提取文件名，表示路径的最后一个部分
        self.file_name = relative_path.split('/')[-1]

    # 创建新的 YAML 文件并设置文件路径
    @catchexcept(f'CbtYaml:setup:')
    def setup(self):
        # 应该是使用文件的所在路径
        if not self.yaml_file_path.parent.exists():
            # 创建存储 YAML 文件的目录，若不存在则递归创建
            self.yaml_file_path.parent.mkdir(parents=True, exist_ok=False)
        if not self.yaml_file_path.exists():
            # 设置 YAML 文件的路径
            self.yaml_file_path.touch()
            logger.info(f'创建文件{self.yaml_file_path}')
        assert self.yaml_file_path.exists()
    # 读取 YAML 文件内容并返回为 Python 数据结构
    @catchexcept(f'CbtYaml:read_yaml:')
    def read_yaml(self) -> Dict:
        with open(self.yaml_file_path, 'r') as file:
            logger.info(f'读取文件{self.yaml_file_path}')
            # 使用 yaml.safe_load 方法解析 YAML 文件
            return yaml.safe_load(file)

    # 将 Python 数据结构写入 YAML 文件
    @catchexcept(f'CbtYaml:write_yaml:')
    def write_yaml(self, data):
        with open(self.yaml_file_path, 'w', encoding='utf-8') as file:
            # 使用 yaml.safe_dump 方法将数据转换成 YAML 格式
            yaml.safe_dump(data, file, allow_unicode=True)
        logger.info(f'写入文件{self.yaml_file_path}')

    # 更新现有的 YAML 文件内容
    @catchexcept(f'CbtYaml:update_yaml:')
    def update_yaml(self, updates):
        # 读取现有 YAML 文件内容
        data = self.read_yaml()
        # 将新的更新内容合并到现有数据中
        data.update(updates)
        # 将更新后的数据写入 YAML 文件
        self.write_yaml(data)
        logger.info(f'更新文件{self.yaml_file_path}')


# 定义CbtModelYaml类，用于处理模型相关的YAML文件
class CbtModelYaml(CbtYaml):
    # 静态属性，设置模型YAML文件的基础路径
    basePath = config.basepath / 'model_yaml'

    # 初始化方法，传入相对路径并调用父类的初始化方法
    def __init__(self, relative_path: str):
        # 调用父类CbtYaml的构造函数，传入模型的基础路径和文件相对路径
        super().__init__(CbtModelYaml.basePath, relative_path=relative_path)


# 定义CbtFlowYaml类，用于处理流程相关的YAML文件
class CbtFlowYaml(CbtYaml):
    # 静态属性，设置流程YAML文件的基础路径
    basePath = config.basepath / 'flow_yaml'

    # 初始化方法，传入相对路径并调用父类的初始化方法
    def __init__(self, relative_path: str):
        # 调用父类CbtYaml的构造函数，传入流程的基础路径和文件相对路径
        super().__init__(CbtFlowYaml.basePath, relative_path=relative_path)


# 定义CbtPipelineYaml类，用于处理GStreamer管道相关的YAML文件
class CbtPipelineYaml(CbtYaml):
    # 静态属性，设置流程YAML文件的基础路径
    basePath = config.basepath / 'gstreamer_yaml'

    # 初始化方法，传入相对路径并调用父类的初始化方法
    def __init__(self, relative_path: str):
        # 调用父类CbtYaml的构造函数，传入流程的基础路径和文件相对路径
        super().__init__(CbtPipelineYaml.basePath, relative_path=relative_path)
