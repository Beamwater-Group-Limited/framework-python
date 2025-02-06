# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : tg
# @File          : data_item.py
# @Author        : henryren
# @Time          : 2024/12/21 10:30
# @Function      : Define a class to represent individual inputs for tasks.
# @Desc          : Each object represents an input block (e.g., text, image, audio).

from enum import Enum
from typing import Dict


class DaFormat(Enum):
    fstring = 'fstring'
    furl = "furl"
    fbase64 = "fbase64"
    fpath = "fpath"

    @staticmethod
    def obj2dct() -> []:
        return [{'label': member.name, 'value': member.value} for member in DaFormat]

    def describe(self):
        descriptions = {
            DaFormat.fstring: "文本类型，用于存储字符串形式的数据。",
            DaFormat.furl: "URL 类型，用于存储资源链接。",
            DaFormat.fbase64: "Base64 类型，用于存储经过 Base64 编码的数据。",
        }
        return descriptions.get(self, "无描述信息。")


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


class DaContent:
    @staticmethod
    def obj2dct(contents: []) -> []:
        return [{'label': con, 'value': con} for con in contents]


# 未使用
class MIMEFormat(Enum):
    plain = "text/plain"  # 纯文本
    html = "text/html"  # HTML 格式
    markdown = "text/markdown"  # Markdown 格式
    png = "image/png"  # PNG 图像格式
    jpeg = "image/jpeg"  # JPEG 图像格式
    jpg = "image/jpeg"  # JPEG 图像格式（缩写形式）
    gif = "image/gif"  # GIF 图像格式
    svg = "image/svg+xml"  # SVG 图像格式
    bmp = "image/bmp"  # BMP 图像格式
    webp = "image/webp"  # WebP 图像格式
    tiff = "image/tiff"  # TIFF 图像格式
    heif = "image/heif"  # HEIF 图像格式
    mp3 = "audio/mpeg"  # MP3 格式音频
    ogg = "audio/ogg"  # OGG 格式音频
    wav = "audio/wav"  # WAV 格式音频
    mp4 = "video/mp4"  # MP4 格式视频
    webm = "video/webm"  # WebM 格式视频
    avi = "video/avi"  # AVI 格式视频
    base64 = "application/base64"  # Base64 编码的内容
    hex = "application/hex"  # Hex 编码格式
    url = "application/url"  # 资源 URL
    csv = "application/csv"  # CSV 文件
    gzip = "application/gzip"  # GZIP 压缩格式
    zip = "application/zip"  # ZIP 压缩格式
    tar = "application/x-tar"  # TAR 格式
    pdf = "application/pdf"  # PDF 文件
    msword = "application/msword"  # Microsoft Word 文档
    ms_excel = "application/vnd.ms-excel"  # Microsoft Excel 文件
    bzip2 = "application/x-bzip2"  # BZIP2 压缩格式
    json = "application/json"  # JSON 格式
    json_ld = "application/ld+json"  # JSON-LD 格式
    yaml = "application/x-yaml"  # YAML 格式
    binary = "application/octet-stream"  # 原始二进制数据
    protobuf = "application/x-protobuf"  # Protocol Buffers 格式
    avro = "application/x-avro"  # Avro 格式
    x_www_form_urlencoded = "application/x-www-form-urlencoded"  # URL 编码的表单数据
    latex = "application/x-latex"  # LaTeX 格式
    rtf = "application/rtf"  # RTF 格式
    gpg = "application/pgp-encrypted"  # GPG 加密格式
    pem = "application/x-pem-file"  # PEM 格式
    form_data = "multipart/form-data"  # 表单数据


class DataItem:
    """
    数据类，用于表示输入信息的单个数据块
    """

    def __init__(self, come_type: DaType = DaType.TEXT, come_format: DaFormat = DaFormat.fstring, content: str = None):
        """
        初始化单个数据块
        :param data_type: 输入类型（如 'text', 'image', 'audio', 等）
        :param data_format: 数据格式（如 'plain', 'base64', 'url', 等）
        :param content: 具体内容（如文本、Base64 编码后的数据）
        """
        self.data_type = come_type.value  # 输入类型
        self.data_format = come_format.value  # 数据格式
        self.content = content  # 输入内容

    def obj2dct(self) -> Dict:
        """
        将对象转换为字典格式
        :return: 字典形式的数据块
        """
        return {
            "type": self.data_type,
            "format": self.data_format,
            "content": self.content,
        }

    # @staticmethod
    # def s2eci(enum_class, member_name):
    #     """
    #     将字符串（大小写不敏感）转换为对应的枚举成员。
    #
    #     :param enum_class: 枚举类
    #     :param member_name: 枚举成员的名称（字符串）
    #     :return: 枚举成员
    #     :raises: ValueError 如果转换失败
    #     """
    #     member_name_upper = member_name.upper()
    #     try:
    #         return enum_class[member_name_upper]
    #     except KeyError:
    #         raise ValueError(f"'{member_name}' 不是有效的 {enum_class.__name__} 枚举成员。")

    @staticmethod
    def as_DataItem(dct: Dict):
        """
        从字典格式恢复 DataItem 对象
        :param dct: 字典对象
        :return: DataItem 实例
        """
        return DataItem(
            # come_type=DaType(dct.get("type", DaType.TEXT.value)),
            come_type=DaType(dct.get("type", None)),
            # come_format= DaFormat(dct.get("format", DaFormat.fstring.value)),
            come_format=DaFormat(dct.get("format", None)),
            content=dct.get("content"),
        )
