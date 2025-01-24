from enum import Enum


class DaType(Enum):
    TEXT = "text"  # 纯文本
    IMAGE = "image"  # 通用图像类型，支持具体格式（如 JPEG, PNG 等）
    AUDIO = "audio"  # 通用音频类型，支持具体格式（如 MP3, WAV 等）
    VIDEO = "video"  # 通用视频类型，支持具体格式（如 MP4, AVI 等)
    APPLICATION = "application"  # 任意文件类型
    FORM_DATA = "multipart/form-data"  # 多部分表单数据

    @staticmethod
    def obj2dct() -> []:
        return [{'label': member.name, 'value': member.value} for member in DaType]


text = "text"
pp = DaType(text)
print(pp.value)