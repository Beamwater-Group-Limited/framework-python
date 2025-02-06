# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_bpmn.py
# @Author        : henryren
# @Time          : 2025/1/19 15:13
# @Function      : 
# @Desc          :
import io
from pathlib import Path

from bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph
from lxml import etree

from app import config
from app.error.PyLogger import pyLogger
from app.error.PyTFError import catchexcept, PyTFError
from app.model.flow.cbt_bpmn_dao import CbtBpmnDao

logger = pyLogger()


class CbtBpmn:
    """
    用于处理 BPMN XML 文件的类，支持文件的读取、写入、更新等操作
    """
    def __init__(self, base_path: Path, relative_path: str):
        """
        初始化方法，设置存储路径、文件路径等属性。
        :param base_path: 基础路径，例如保存 BPMN 文件的根目录
        :param relative_path: 相对路径，指向具体 BPMN 文件的路径
        """
        self.base_path = base_path
        self.relative_path = relative_path
        self.file_path = base_path / relative_path  # 完整文件路径
        self.file_name = relative_path.split('/')[-1]  # 文件名
        self.organize_name = relative_path.split('/')[0]  # 从路径中提取组织名
        self.diagram = None
        # 内容
        self.xml_content = None
        # 树
        self.bpmn_tree = None

    @catchexcept(f'CbtBpmn:setup:')
    def setup(self):
        """
        创建文件目录和文件（如果不存在）。如果文件存在
        """
        if not self.file_path.parent.exists():
            # 创建目录（如果不存在）
            self.file_path.parent.mkdir(parents=True, exist_ok=False)
        if not self.file_path.exists():
            # 创建文件（如果不存在）
            self.file_path.touch()
            logger.info(f'创建文件 {self.file_path}')
        assert self.file_path.exists(), f"BPMN 文件未成功创建: {self.file_path}"

    @catchexcept(f'CbtBpmn:read_bpmn:')
    def read_bpmn(self)->str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            logger.info(f'读取文件{self.file_path}')
            # 使用 yaml.safe_load 方法解析 YAML 文件
            self.xml_content = file.read()
            return self.xml_content

    @catchexcept(f'CbtBpmn:read_bpmn_tree:')
    def read_bpmn_tree(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            logger.info(f'读取文件{self.file_path}')
            self.xml_content = file.read()
            self.bpmn_tree = CbtBpmn.load_from_unicode_str(self.xml_content)
            return self.bpmn_tree

    @catchexcept(f'CbtBpmn:write_bpmn:')
    def write_bpmn(self, xml_content: str):
        # 将树保存到文件，并设置缩进和编码
        with open(self.file_path, "w", encoding='utf-8') as file:
            self.xml_content = xml_content
            file.write(self.xml_content)
        print(f"XML 文件已成功写入到: {self.file_path}")

    @staticmethod
    @catchexcept(f'CbtBpmn:parse_bpmn:')
    def load_from_unicode_str(bpmn_str:str):
        # 将字符串编码为字节
        bpmn_bytes = bpmn_str.encode("utf-8")
        bpmn_tree = etree.fromstring(bpmn_bytes)
        return bpmn_tree

# 定义 CbtFlowBpmn 类来具体处理流程相关的 BPMN 文件
class CbtFlowBpmn(CbtBpmn):
    base_path = config.basepath / 'flow_bpmn'  # 基础路径
    namespaces = {'bpmn2': 'http://www.omg.org/spec/BPMN/20100524/MODEL'} # bpmn2空间
    def __init__(self, relative_path: str = None, author: str = None, file_name: str = None):
        """
        初始化流程相关 BPMN 文件的处理类。
        :param relative_path: 相对路径，例如 `cbtai/example.bpmn`
        """
        if relative_path is None:
            relative_path = f'{author}/{file_name}.bpmn'
        super().__init__(CbtFlowBpmn.base_path, relative_path)

    @catchexcept(f'CbtFlowBpmn:get_flow:')
    def get_flow_dao(self) -> CbtBpmnDao:
        self.bpmn_tree = self.read_bpmn_tree()
        process = CbtFlowBpmn.get_process(self.bpmn_tree)
        bpmn_description = process.get("name", None)
        bpmn_author: str = self.organize_name
        bpmn_name: str = process.get("id", None)
        cbtBpmnDao = CbtBpmnDao(bpmn_description=bpmn_description,bpmn_author=bpmn_author,bpmn_name=bpmn_name)
        return cbtBpmnDao

    @catchexcept(f'CbtFlowBpmn:find_incoming:')
    def find_incoming(self, element_id:str)->[]:
        self.bpmn_tree = self.read_bpmn_tree()
        task_node = CbtFlowBpmn.find_incoming_node(self.bpmn_tree, element_id=element_id)
        if task_node is None or len(task_node) == 0:
            return []
        tag_name = etree.QName(task_node.tag).localname
        params = None
        if tag_name == 'startEvent':
            params = task_node.get('{http://magic}inputparams', None)
        if tag_name == 'userTask':
            params = task_node.get('{http://cbtai}downParams', None)
        if params is None or len(params) == 0:
            return []
        contents = [param.split('→')[-1] for param in params.split('✓')]
        return contents



    @staticmethod
    @catchexcept(f'CbtFlowBpmn:create_from_dao:')
    def create_from_dao(cbtBpmnDao:CbtBpmnDao,bpmnDiagramGraph:BpmnDiagramGraph)->str:
        # 创建文件
        cfb = CbtFlowBpmn(relative_path=f'{cbtBpmnDao.bpmn_author}/{cbtBpmnDao.bpmn_name}.bpmn')
        cfb.setup()
        cfb.write_bpmn(diagram=bpmnDiagramGraph)
        logger.info(f'根据指定的信息，创建了一个新的流的bpmn文件: {cfb.file_path}')
        return str(cfb.file_path)
    @staticmethod
    @catchexcept(f'CbtFlowBpmn:get_process_id_first:')
    def get_process_id_first(bpmn_tree)->str:
        # 获取process id
        # 查找所有 <process> 节点
        processes = bpmn_tree.xpath("//bpmn2:process/@id", namespaces=CbtFlowBpmn.namespaces)
        logger.info(f'加载的流程节点: {processes}')
        assert len(processes) > 0, logger.info(f'加载的流程节点数量为0: {processes}')
        return processes[0]
    @staticmethod
    @catchexcept(f'CbtFlowBpmn:get_process:')
    def get_process(bpmn_tree):
        # 获取process id
        # 查找所有 <process> 节点
        processes = bpmn_tree.xpath("//bpmn2:process", namespaces=CbtFlowBpmn.namespaces)
        logger.info(f'加载的流程节点: {processes}')
        assert len(processes) > 0, logger.info(f'加载的流程节点数量为0: {processes}')
        return processes[0]

    @staticmethod
    @catchexcept(f'CbtFlowBpmn:get_task_with_id:')
    def get_task_with_id(bpmn_tree, task_id:str):
        # 1. 查找任务节点
        task_xpath = f"//bpmn2:*[@id='{task_id}']"  # 匹配任何带有特定 ID 的节点
        task_node = bpmn_tree.xpath(task_xpath, namespaces=CbtFlowBpmn.namespaces)
        if not task_node:
            raise ValueError(f"任务 ID '{task_id}' 未找到")
        # 任务节点是唯一的
        return task_node[0]

    @staticmethod
    @catchexcept(f'CbtFlowBpmn:find_incoming_node:')
    def find_incoming_node(bpmn_tree, element_id:str):
        # 2. 查找连入的 sequenceFlow
        sequence_flow_xpath = f"//bpmn2:sequenceFlow[@targetRef='{element_id}']"
        incoming_flows = bpmn_tree.xpath(sequence_flow_xpath, namespaces=CbtFlowBpmn.namespaces)
        if not incoming_flows:
            return []
        source_ref = incoming_flows[0].get("sourceRef")
        if not source_ref :
            return []
        # 查找 sourceRef 对应的节点
        source_node_xpath = f"//bpmn2:*[@id='{source_ref}']"
        source_nodes = bpmn_tree.xpath(source_node_xpath, namespaces=CbtFlowBpmn.namespaces)
        if not source_nodes:
            return []
        return source_nodes[0]

