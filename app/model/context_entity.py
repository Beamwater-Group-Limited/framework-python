# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : tg
# @File          : context_entity.py
# @Author        : henryren
# @Time          : 2024/12/21 11:00
# @Function      : Define a class to manage context-related information.
# @Desc          : This entity stores user details and additional context metadata.

from typing import Dict


class ContextEntity:
    """
    数据类，用于表示上下文信息，包括用户和元数据
    """

    def __init__(self, user: Dict[str, str] = None, metadata: Dict[str, str] = None):
        """
        初始化上下文信息
        :param user: 用户信息（如 ID 和角色）
        :param metadata: 元数据（如来源和 IP 地址）
        """
        self.user = user if user else {}  # 用户信息
        self.metadata = metadata if metadata else {}  # 元数据

    def obj2dct(self) -> Dict:
        """
        将 ContextEntity 转换为字典格式
        :return: 字典形式的上下文
        """
        return {
            "user": self.user,
            "metadata": self.metadata,
        }

    @staticmethod
    def as_ContextEntity(dct: Dict):
        """
        从字典格式恢复 ContextEntity 对象
        :param dct: 字典对象
        :return: ContextEntity 实例
        """
        return ContextEntity(
            user=dct.get("user", {}),
            metadata=dct.get("metadata", {})
        )