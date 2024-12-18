# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : docker_ssd_mobilenet
# @File          : config.py
# @Author        : wen
# @Time          : 2022/12/29 13:51
# @Function      : 配置文件
# @Desc          : 配置路径

import logging
import traceback
import yaml
from pathlib import Path

try:
    con = yaml.safe_load(Path('config/application.yaml').open())
    app_name = con['app_name']
    log_level = logging.getLevelName(con['log_level'])
    projid = con['projid']
    # 从配置文件载入
    basepath = Path(con['basepath'])
    port = con['baseport']
    baseurl = con['baseurl']
    host = con['baseurl'] + (f':{port}' if str(port) != "" else '')
    # 图床模块名 缩略图路径等使用
    picmoudle = con['picmoudle']
    picmoudle = picmoudle if picmoudle is not None else ''
    # 修复 bug None
    # rabbitmq
    sourceip = con['rabbitmq']['sourceip']
    amqpport = con['rabbitmq']['amqpport']
    myvhost = con['rabbitmq']['myvhost']
    queue = con['rabbitmq']['queue']
    celery_broker = f'amqp://guest@{sourceip}:{amqpport}/{myvhost}'
    celery_backend = 'rpc://'
    print(f'配置环境:')
    print(f'app_name:{app_name}')
    print(f'log_level:{log_level}')
    print(f'projid:{projid}')
    print(f'basepath:{basepath}')
    print(f'port:{port}')
    print(f'host:{host}')
    print(f'picmoudle:{picmoudle}')
    print(f'queue:{queue}')
    print(f'celery_broker:{celery_broker}')
    print(f'celery_backend:{celery_backend}')
except BaseException:
    traceback.print_exc()
    print(f'配置文件 application.yaml 加载失败')
