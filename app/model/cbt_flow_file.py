# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_flow_file.py
# @Author        : henryren
# @Time          : 2025/1/15 17:45
# @Function      : 
# @Desc          : 流文件管理
from app.error.PyLogger import pyLogger
from app.error.PyTFError import catchexcept
from app.model.cbt_flow_dao import CbtFlowDao
from app.model.file.cbt_yaml import CbtFlowYaml

logger = pyLogger()
class CbtFlowFile:
    # 初始化CbtModelFile类
    def __init__(self,flow_author:str) -> None:
        # 定义模型的基础路径为配置中的hub路径
        self.flow_base_path = CbtFlowYaml.basePath / flow_author
        # 存储模型信息的列表
        self.flow_daos = None
        # 默认用户
        self.flow_author = flow_author

    # 获取所有模型目录及其信息
    @catchexcept(f'CbtFlowFile:scanFlowYamlDir')
    def scanFlowYamlDir(self) -> []:
        self.flow_daos = []
        # 遍历模型基础路径下的所有文件
        files = [file for file in self.flow_base_path.rglob('*') if file.suffix == '.yaml']
        if len(files) == 0:
            # 创建一个默认流
            default_flow  = CbtFlowDao(f'{self.flow_author}/default.yaml')
            # 开始点 配置输入项
            # n个输入
            # n 个输出
            # 加载所有接口
            # 获取需要的接口
            default_flow_yaml = CbtFlowYaml(f'{self.flow_author}/default.yaml')
            default_flow_yaml.setup()
            default_flow_yaml.write_yaml(default_flow.obj2dct())
        else:
            for file in files:
                flow_yaml = CbtFlowYaml(f'{self.flow_author}/{file.name}')
                flow_dict = flow_yaml.read_yaml()
                self.flow_daos.append(CbtFlowDao.as_CbtFlowDao(flow_dict))
        # 返回所有收集的模型信息
        return self.flow_daos

