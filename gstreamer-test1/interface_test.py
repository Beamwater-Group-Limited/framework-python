import json
from enum import Enum
from typing import Dict

import requests

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

# 需要预先配置的
def pyLoggerFirst():
    logger = logging.getLogger("121212121")
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
    logger = logging.getLogger("111111")
    return logger

"""
# 创建一个 DataItem 对象实例
data_item_instance = DataItem(
    come_type=DaType.TEXT,  # 数据类型为文本
    come_format=DaFormat.fstring,  # 数据格式为字符串
    content="This is a sample text content."  # 实际内容
)
1. **`come_type`**:
    - `DaType.TEXT` 表示数据类型为文本（如文本文字）。
    - 其他选项可以是 `IMAGE`、`AUDIO`、`VIDEO` 等。

2. **`come_format`**:
    - `DaFormat.fstring` 表示字符串形式的内容格式。
    - 其他选项可以是 `furl`（URL）、`fpath`（文件路径）等。

3. **`content`**:
    - 实际的数据内容，在本例中是简单的一段文本。
"""

class DaFormat(Enum):
    fstring = 'fstring'
    furl = "furl"
    fbase64 = "fbase64"
    fpath = "fpath"

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
            come_type=DaType(dct.get("type", DaType.TEXT.value)),
            come_format= DaFormat(dct.get("format", DaFormat.fstring.value)),
            content=dct.get("content"),
        )

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


import uuid
from datetime import datetime
from typing import Dict

# 主要的开发任务就是撰写和调试系统提示词，然后使用数据集来进行验证
system_promt = """你是一个模拟 RESTful 风格 API 的服务端。当用户发送请求时，你需要根据请求内容生成相应的回复，并将其包装成符合 RESTful API 规范的 JSON 格式。所有的回复必须严格遵循以下格式，不能包含任何其他形式的内容。

### 成功响应格式：
{
  "respon_status": "success",
  "data": {
    // 根据具体请求返回的数据内容
  }
}

### 错误响应格式：
{
  "respon_status": "error",
  "message": "错误描述信息"
}

### 响应要求：
1. **严格遵循 JSON 格式**：所有回复必须是有效的 JSON，不得包含任何额外的文字、解释或格式。
2. **状态字段**：
   - 成功时，`respon_status` 字段的值为 `"success"`，并包含一个 `data` 字段，用于存放具体的数据。
   - 发生错误时，`respon_status` 字段的值为 `"error"`，并包含一个 `message` 字段，用于描述错误信息。
3. **数据字段**：
   - 在成功响应中，`data` 字段应根据请求内容动态生成，确保数据的完整性和准确性。
4. **错误处理**：
   - 对于无效请求、参数错误、资源未找到等情况，返回符合错误响应格式的 JSON，并提供明确的错误描述。

### 示例：

**请求：**
获取用户信息，用户ID为12345

**成功响应：**
{
  "respon_status": "success",
  "data": [
        {
            "come_type"="TEXT",
            "come_format"="fstring",
            "content"="This is a sample text content."
        },
        {
            "come_type"="TEXT",
            "come_format"="fstring",
            "content"="这是一个例子"
        },
        {
            "come_type"="TEXT",
            "come_format"="fstring",
            "content"="{
                            \"name\": \"zs\",
                            \"age\": 20,
                            \"gender\": \"男\",
                            \"address\": None,
                            \"hobby\": [\"吃饭\", \"睡觉\", \"打豆豆\"]
                        }"
        },
  ]
}

**请求：**
获取用户信息，用户ID为不存在的ID

**错误响应：**
{
  "respon_status": "error",
  "message": "用户未找到"
}

### 注意事项：
- 无论请求内容为何，所有回复必须严格按照上述 JSON 格式进行。
- 不要在回复中添加任何额外的说明、注释或格式化内容。
- 确保 JSON 的语法正确，无语法错误。

请根据以上要求处理接下来的所有请求，并确保回复的每一个响应都符合上述规范。
"""
# 示范的一个请求数据 come_data 中的 comes
"""
# 示例协议范例
image_url = "https://www.baidu.com/img/bd_logo1.png"
comes = {
    DataItem(content="process"),
    DataItem(content=system_promt),
    DataItem(DaType.IMAGE,DaFormat.furl,content=f"{image_url}"),
    DataItem(content="图片中的内容是什么")
}
"""


class ComeEntity:
    def __init__(self):
        self.id = None  # 请求 ID，用于跟踪/排错
        self.timestamp = None  # 发起请求时间（ISO8601 格式）
        self.model = None  # 指定大模型的版本或引擎
        self.respon_status = None  # 返回状态
        self.comes = None  # 多模态输入，可以存储多个图文/音频等数据块
        self.context = None  # 其他上下文信息（与用户有关）

    def setup(
            self,
            comes: [DataItem],
            respon_status: str = 'OK',
            context: ContextEntity = None,
    ) -> 'ComeEntity':
        """
        设置输入参数.
        :param id: 请求 ID
        :param timestamp: 请求时间，可以是字符串或 datetime 对象
        :param model: 使用的大模型版本或引擎
        :param respon_status: 指定返回状态
        :param comes: 输入信息数组（支持 text, image 等）
        :param context: 上下文信息（如用户和元数据）
        :return: 返回 self
        """

        self.id = str(uuid.uuid4()).replace('-', '')[:8]
        self.timestamp = datetime.now().isoformat()
        self.model = 'llava-hf/llava-onevision-qwen2-7b-ov-hf'
        self.respon_status = respon_status
        self.comes = comes
        self.context = context
        return self

    def obj2dct(self) -> Dict:
        """
        将对象转化为字典格式，以用于序列化/传输.
        :return: 字典格式的 ComeEntity
        """
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "model": self.model,
            "respon_status": self.respon_status,
            "comes": [di.obj2dct() for di in self.comes],
            "context": self.context.obj2dct(),
        }

    @staticmethod
    def as_ComeEntity(dct: Dict):
        """
        从字典重新构建对象
        :param dct: 字典输入
        :return: 重建的 ComeEntity 对象
        """
        con = ComeEntity()
        con.id = dct.get("id")
        con.timestamp = dct.get("timestamp")
        con.model = dct.get("model")
        con.respon_status = dct.get("respon_status")
        con.comes = [DataItem.as_DataItem(di) for di in dct.get("comes", [])]
        con.context = ContextEntity.as_ContextEntity(dct.get("context", {}))
        return con


def llava():
    logger = pyLoggerFirst()

    cheng_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "come_type": {
                    "type": "string"
                },
                "come_format": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                }
            },
            "required": ["come_type", "come_format","content"],
            "additionalProperties": False  # 不允许额外的字段
        },
    }
    # todo 增加本地数据测试
    image_left = "https://www.baidu.com/img/bd_logo1.png"
    image_right = "http://images.cocodataset.org/val2017/000000039769.jpg"
    # image_quest = "https://q6.itc.cn/q_70/images03/20240229/d3f2bf2b8bb24f65bebf0e9e1b7e8910.jpeg"
    # 创建数据
    comes = [
        DataItem(content="process"),
        DataItem(DaType.APPLICATION,DaFormat.fstring,content=json.dumps(cheng_schema)),
        DataItem(content='关于图片的问题的回答字数不要超过 10个字'),
        # DataItem(DaType.IMAGE, DaFormat.furl, content=f"{image_left}"),
        DataItem(DaType.IMAGE, DaFormat.furl, content=f"{image_right}"),
        # DataItem(DaType.IMAGE, DaFormat.furl, content=f"{image_right}"),
        DataItem(content="描述一下图片内容\n")
    ]
    comeEntity =  ComeEntity().setup(comes=comes,context=ContextEntity())
    # 定义请求的 URL
    url = "http://192.168.0.70:28286/v1/process"  # 替换为目标 URL

    # 定义 JSON 数据
    payload = comeEntity.obj2dct()
    # 发送 POST 请求
    headers = {"Content-Type": "application/json"}
    logger.debug(f'url:\n{url}')
    logger.debug(f'payload:\n{payload}')
    logger.debug(f'headers\n{headers}')
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    hao_comeEntity = ComeEntity.as_ComeEntity(response.json())
    logger.debug(f'响应:{hao_comeEntity.obj2dct()}')
    return

llava()
