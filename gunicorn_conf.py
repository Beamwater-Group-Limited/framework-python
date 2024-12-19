# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : docker_ssd_mobilenet
# @File          : gunicorn_conf.py
# @Author        : henryren
# @Time          : 2021/2/24 01:22
# @Function      : 
# @Desc          :
# 绑定ip和端口号
import os

bind = '0.0.0.0:8080'
os.environ["g_host"] = f'0.0.0.0'
os.environ["g_port"] = f'8080'
workers = 1
worker_class = 'sync' # 因为避开线程 所以不能使用gevent模式，默认的是sync模式
#超时
timeout = 300000
loglevel = 'debug'
# 设置gunicorn访问日志格式，错误日志无法设置
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# accesslog = "/var/log/gunicorn_access.log"      #访问日志文件
accesslog = "-"      #访问日志文件
# errorlog = "/var/log/gunicorn_error.log"        #错误日志文件