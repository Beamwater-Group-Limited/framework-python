# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : PyTFError.py
# @Author        : henryren
# @Time          : 2024/6/3 13:12
# @Function      : 
# @Desc          :
import asyncio
import traceback
from functools import wraps

import falcon

from app.error.PyLogger import pyLogger

logger = pyLogger()



class PyTFError(BaseException):
    # 自定义错误页面 HTML
    error_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>错误</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f8f9fa;
                        color: #212529;
                        text-align: center;
                        padding: 50px;
                    }
                    .container {
                        max-width: 600px;
                        margin: auto;
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                        color: #dc3545;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>错误 400: 无效请求</h1>
                    <p>抱歉，您的请求出现了问题。</p>
                </div>
            </body>
            </html>
            """
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
        self.message = message

    @classmethod
    def msg(cls, message: str):
        return cls(message, "err")

# 定义支持异步的异常捕获装饰器
def catchexcept(log_message="发生PyTFError异常:"):
    """
    装饰器，用于捕获被装饰函数中的所有异常，兼容同步和异步函数。

    参数:
        log_message (str): 捕获异常时记录的日志前缀
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                # 处理异步函数
                return await func(*args, **kwargs)
            except Exception as e:
                traceback.format_exc()
                logger.error(f"{log_message}{e}", exc_info=True)
                # 抛出自定义异常
                raise PyTFError(f'{log_message}', e)


        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                # 处理同步函数
                return func(*args, **kwargs)
            except Exception as e:
                traceback.format_exc()
                logger.error(f"{log_message}{e}", exc_info=True)
                # 抛出自定义异常
                raise PyTFError(f'{log_message}', e)
        # 根据是否为协程函数，选择适当的包装器
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def catchexceptpage(log_message ="发生 PyTFError 异常"):
    """
    装饰器，用于捕获异步或同步视图函数中的所有异常，并设置错误响应。

    参数:
        log_message (str): 捕获异常时记录的日志前缀
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(req, resp, *args, **kwargs):
            try:
                # 处理异步函数逻辑
                return await func(req, resp, *args, **kwargs)
            except Exception as e:
                raise falcon.HTTPError

        @wraps(func)
        def sync_wrapper(req, resp, *args, **kwargs):
            try:
                # 处理同步函数逻辑
                return func(req, resp, *args, **kwargs)
            except Exception as e:
                raise falcon.HTTPError

        # 判断目标函数是否为异步函数，并选择适配的包装函数
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator