# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_model_file.py
# @Author        : henryren
# @Time          : 2025/1/9 18:53
# @Function      : 
# @Desc          :

from app import config
from app.error.PyLogger import pyLogger
from app.model.model.cbt_model_info_dao import CbtModelInfoDao
from app.model.file.cbt_yaml import CbtModelYaml

logger = pyLogger()
class CbtModelFile:
    # 初始化CbtModelFile类
    def __init__(self) -> None:
        # 定义模型的基础路径为配置中的hub路径
        self.model_base_path = config.basepath / 'hub'
        # 存储模型信息的列表
        self.model_infos = None

    # 获取所有模型目录及其信息
    def scanModelDir(self) -> []:
        self.model_infos = []
        # 遍历模型基础路径下的所有文件夹
        for model_dir in self.model_base_path.iterdir():
            # 如果当前路径是文件夹
            if model_dir.is_dir() and (model_dir / 'snapshots').exists():
                # 检查'版本'文件夹是否存在
                for revision in (model_dir / 'snapshots').iterdir():
                    # 从目录名称中提取公司名称和模型名称
                    company_name, model_name = tuple(model_dir.name.split('--')[1:])
                    # 如果修订版本存在，则获取其名称
                    if revision:
                        revision = revision.name
                        # 构造模型信息
                        cm_info = CbtModelInfoDao(
                            company_name=company_name,
                            model_name=model_name,
                            revision=revision
                        )
                        # facebook   bart-base/
                        cm_info_yaml = CbtModelYaml(cm_info.model_config_path)
                        cm_info_yaml.setup()
                        if cm_info_yaml.yaml_file_path.exists():
                            cm_all_info = cm_info_yaml.read_yaml()
                            # 创建CbtModelInfo实例并添加到模型信息列表中
                            self.model_infos.append(cm_all_info)
                        else:
                            cm_info_yaml.write_yaml(cm_info.obj2dct())
                            self.model_infos.append(cm_info.obj2dct())
        # 返回所有收集的模型信息
        return self.model_infos