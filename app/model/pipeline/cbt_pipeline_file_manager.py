# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_bpmn_file.py
# @Author        : henryren
# @Time          : 2025/1/19 15:39
# @Function      : 
# @Desc          : 
from pathlib import Path

from app.error.PyLogger import pyLogger
from app.error.PyTFError import catchexcept
from app.model.file.cbt_yaml import CbtPipelineYaml
from app.model.pipeline.cbt_pipeline_dao import CbtPipelineDao

logger = pyLogger()


class CbtPipelineFileManager:
    """
    基于 YAML 的文件管理模块，提供创建、扫描、读取和更新功能
    """
    # 定义 YAML 文件的默认文件
    yaml_default = '123.yaml'
    def __init__(self, author: str) -> None:
        # 定义 GStreamer管道的 YAML 文件的基础路径
        self.yaml_base_path = CbtPipelineYaml.basePath / author
        # 用户名，即文件所属的作者
        self.author = author
        # YAML 文件的信息列表
        self.yaml_daos = None

    @catchexcept(f'CbtPipelineFileManager:scanPipelineDir')
    def scanPipelineDir(self) -> list:
        """
        扫描用户目录下的所有 YAML 文件并加载其信息
        :return: YAML 数据对象的列表
        """
        self.yaml_daos = []
        # 获取当前用户目录下的所有 `.yaml` 文件
        files = [file for file in self.yaml_base_path.rglob('*') if file.suffix == '.yaml']
        # 如果没有 yaml 文件，则创建一个默认 yaml 文件
        if len(files) == 0:
            print("初始化默认yaml文件")
            # logger.info(f"未找到 YAML 文件，为用户 {self.author} 创建默认文件。")
            # # 获取公共的初始化
            # public_default_bpmn = CbtPipelineYaml(CbtPipelineFileManager.yaml_default)
            # public_default_bpmn_graph = public_default_bpmn.read_bpmn()
            # # 生成用户下默认
            # default_bpmn_graph = CbtFlowBpmn(f'{self.author}/default.bpmn')
            # default_bpmn_graph.setup()
            # default_bpmn_graph.write_bpmn(public_default_bpmn_graph)
        else:
            # 遍历 `yaml` 文件并加载 YAML 数据
            for file in files:
                yaml_graph = CbtPipelineYaml(f'{self.author}/{file.name}').read_yaml()
                yaml_dao = CbtPipelineDao().as_CbtPipelineDao(yaml_graph)
                self.yaml_daos.append(yaml_dao.obj2dct())
        return self.yaml_daos

    # @catchexcept(f'CbtBpmnFileManager:createNewBpmn')
    # def createNewBpmn(self, flow_describe: str,author:str) -> str:
    #     # 初始化一个 BPMN 图对象
    #     diagram = BpmnDiagramGraph()
    #     # 创建一个新的 BPMN 图
    #     diagram.create_new_diagram_graph()
    #     # 添加流程到 BPMN 图中，流程 ID 自动生成，不能自定义
    #     process_id = diagram.add_process_to_diagram(process_name=flow_describe)
    #     # 创建 BPMN DAO 对象，用于存储 BPMN 文件的属性和内容
    #     # 这里的流程描述、作者和流程 ID 需要一一对应
    #     cbd = CbtBpmnDao(bpmn_description=flow_describe, bpmn_author=author, bpmn_name=process_id)
    #     # 为流程添加一个开始事件，事件名称为 "Input Parameters"
    #     diagram.add_start_event_to_diagram(process_id=process_id, start_event_name='Cbt Input Parameters')
    #     # 根据 DAO 对象和 BPMN 图生成 BPMN 文件，并返回文件路径
    #     bpmn_file_path = CbtFlowBpmn.create_from_dao(cbtBpmnDao=cbd, bpmnDiagramGraph=diagram)
    #     # 返回生成的 BPMN 文件路径
    #     return bpmn_file_path