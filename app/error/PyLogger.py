# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pyfinetune
# @File          : PyLogger.py
# @Author        : henryren
# @Time          : 2024/11/18 12:23
# @Function      : 
# @Desc          : 构造日志
import logging

import colorlog

from app import config

# 需要预先配置的
def pyLoggerFirst():
    logger = logging.getLogger(config.app_name)
    # 配置日志模块的信息标准【什么等级的信息会被捕捉】
    logger.setLevel('DEBUG')
    # 配置日志颜色
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # 配置日志模块的处理器【处理日志模块捕捉到的等级】
    logger.addHandler(handler)
    logger.propagate = False
    return logger


# 已经配置过了的，直接使用
def pyLogger():
    logger = logging.getLogger(config.app_name)
    return logger
