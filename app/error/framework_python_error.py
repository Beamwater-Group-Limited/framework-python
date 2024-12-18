# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : framework-python
# @File          : FrameWorkPythonError
# @Author        : Yuan
# @Time          : 2024/12/18 15:24
# @Function      :
# @Desc          :
class FrameWorkPythonError(BaseException):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

    @classmethod
    def msg(cls, message: str):
        return cls(message, "err")

