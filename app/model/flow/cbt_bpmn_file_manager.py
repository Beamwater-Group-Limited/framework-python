# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_bpmn_file.py
# @Author        : henryren
# @Time          : 2025/1/19 15:39
# @Function      : 
# @Desc          : 
from pathlib import Path

from bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph

from app.error.PyLogger import pyLogger
from app.error.PyTFError import catchexcept
from app.model.file.cbt_bpmn import CbtFlowBpmn
from app.model.flow.cbt_bpmn_dao import CbtBpmnDao  # 假设 BPMN 数据对象类（用于存储 BPMN 的信息和数据）

logger = pyLogger()


class CbtBpmnFileManager:
    """
    基于 BPMN 的文件管理模块，提供创建、扫描、读取和更新功能
    """
    # 定义 BPMN 文件的默认文件
    bpmn_default = 'newDiagram.bpmn'
    def __init__(self, author: str) -> None:
        # 定义 BPMN 文件的基础路径
        self.bpmn_base_path = CbtFlowBpmn.base_path / author
        # 用户名，即文件所属的作者
        self.author = author
        # BPMN 文件的信息列表
        self.bpmn_daos = None

    @catchexcept(f'CbtBpmnFileManager:scanBpmnDir')
    def scanBpmnDir(self) -> list:
        """
        扫描用户目录下的所有 BPMN 文件并加载其信息
        :return: BPMN 数据对象的列表
        """
        self.bpmn_daos = []
        # 获取当前用户目录下的所有 `.bpmn` 文件
        files = [file for file in self.bpmn_base_path.rglob('*') if file.suffix == '.bpmn']
        # 如果没有 BPMN 文件，则创建一个默认 BPMN 文件
        if len(files) == 0:
            logger.info(f"未找到 BPMN 文件，为用户 {self.author} 创建默认文件。")
            # 生成用户下默认
            default_bpmn = CbtFlowBpmn(f'{self.author}/process_1.bpmn')
            default_bpmn.write_bpmn(CbtFlowBpmn(relative_path=CbtBpmnFileManager.bpmn_default).read_bpmn())
            self.bpmn_daos.append(default_bpmn.get_flow_dao())
        else:
            for file in files:
                bpmn_dao = CbtFlowBpmn(f'{self.author}/{file.name}').get_flow_dao()
                self.bpmn_daos.append(bpmn_dao)
        return self.bpmn_daos

    @catchexcept(f'CbtBpmnFileManager:createNewBpmn')
    def createNewBpmn(self, flow_describe: str,author:str) -> str:
        # 初始化一个 BPMN 图对象
        diagram = BpmnDiagramGraph()
        # 创建一个新的 BPMN 图
        diagram.create_new_diagram_graph()
        # 添加流程到 BPMN 图中，流程 ID 自动生成，不能自定义
        process_id = diagram.add_process_to_diagram(process_name=flow_describe)
        # 创建 BPMN DAO 对象，用于存储 BPMN 文件的属性和内容
        # 这里的流程描述、作者和流程 ID 需要一一对应
        cbd = CbtBpmnDao(bpmn_description=flow_describe, bpmn_author=author, bpmn_name=process_id)
        # 为流程添加一个开始事件，事件名称为 "Input Parameters"
        diagram.add_start_event_to_diagram(process_id=process_id, start_event_name='Cbt Input Parameters')
        # 根据 DAO 对象和 BPMN 图生成 BPMN 文件，并返回文件路径
        bpmn_file_path = CbtFlowBpmn.create_from_dao(cbtBpmnDao=cbd, bpmnDiagramGraph=diagram)
        # 返回生成的 BPMN 文件路径
        return bpmn_file_path