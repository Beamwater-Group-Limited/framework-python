# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : docker_ssd_mobilenet
# @File          : gunicorn_conf.py
# @Author        : wen
# @Time          : 2022/12/28 14:49
# @Function      :
# @Desc          :
# 绑定ip和端口号
bind = '0.0.0.0:8080'
workers = 1
worker_class = 'sync' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
#超时
timeout = 300000
loglevel = 'debug'
# 设置gunicorn访问日志格式，错误日志无法设置
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# accesslog = "/var/log/gunicorn_access.log"      #访问日志文件
accesslog = "-"      #访问日志文件
# errorlog = "/var/log/gunicorn_error.log"        #错误日志文件